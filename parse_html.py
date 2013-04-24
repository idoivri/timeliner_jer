import re
import requests
import csv
import sys
from bs4 import BeautifulSoup
import json

# A helper function to extract year string from year
def _extract_year(str):
	#try to find a four-digit year
	match = re.search(r'\d{4}', str)
	if match:
		return match.group(0)
	else: #try finding a four-digit year

		match = re.search(r'\d{3}', str)
		if match:
			return match.group(0)+"5" #for 192- return 1925

		else: #try finding a two-digit year
			match = re.search(r'\d{2}', str)
			if match:
				return match.group(0)+"00" #for 19-- return 1900

	return None

def _year_to_date(year):
	return "1/1/%s 0:00:00" % year


# # A helper function to write the URL/Year dictionary to a CSV file 
# Start Date, End Date, Headline, Text,	Media, Media Credit, Media Caption,	Media Thumbnail, Type, Tag
# def output_csv(mapsDictionary):
#     for i in mapsDictionary:
#     	# out = json.dumps(i, ensure_ascii=False)
#     	out ='"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"' % \
#     		(i[3], i[4], json.dumps(i[2], ensure_ascii=False), json.dumps(i[2], ensure_ascii=False), i[1], 'media credit', i[0], 'type', 'tag')
#     	print out.encode('utf-8')
    	

# # # A helper function to write the URL/Year dictionary to a CSV file 
# # Start Date, End Date, Headline, Text,	Media, Media Credit, Media Caption,	Media Thumbnail, Type, Tag
def output_csv(mapsDictionary):

    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)

    for i in mapsDictionary:
        writer.writerow( (i[4], i[5], i[2].encode('utf-8'), i[3].encode('utf-8'), i[1], 'National Library of Israel', i[1], 'type', 'tag') )


def get_details(url):
	i = requests.get(url)
	bs = BeautifulSoup(i.text)
	image_url = bs.find('img', {'class':'imgthumb'}).parent.get('href')


	notes = [] ; headline = '' ; text = ''
	for n in bs.find_all(text="Note"):
		notes.append(n.find_next('td').text)

	if len(notes) == 1:
		headline = notes[0]

	elif len(notes) > 1:
		notes.append(notes.pop(0)) # turns out first line is usually less interesting - move it to last
		headline = notes.pop(0)
		text = '\n'.join(notes)

	# for n in bs.find_all(text="Note"):
	# 	notes += ' ' + n.find_next('td').text

	# print notes

	return image_url, headline, text


r = requests.get('http://www.jnul.huji.ac.il/dl/maps/jer/html/date.html')

if r.status_code != 200:
	print "Failed to open URL. Status code: %s" % r.status_code
	exit()

soup = BeautifulSoup(r.text)

data = soup.find("table", cols="5")

table = data.find_all('tr')

numCols = 5; #there are 5 columns in the map webpage

urlYearDictionary = [] #dictionary to contain url,year,label triples

for i in range(len(table)):

	if i%2==0:

		res = [[] for _ in range(numCols)] #create a dictionary of 5 items representing 5 maps: [ [url,year,label] * 5 ]

		#fill in the map URLs:
		tempList = table[i].find_all("td");

		for j in range(numCols):

			img_url = tempList[j].find_next("img").get('src')
			res[j].append(img_url)
			info_url = 'http://www.jnul.huji.ac.il/dl/maps/jer/html/' + tempList[j].find_next("a").get('href')

			image_url, headline, text = get_details(info_url)
			res[j].append(image_url)
			res[j].append(headline)
			res[j].append(text)

			# print info_url
			# detail_urls.append(info_url)
			# print img_url

		#fill in the map year attributes:
		tempList = table[i+1].find_all("td");

		for j in range(numCols):
			y = _extract_year(tempList[j].text)
			year = _year_to_date(y)

			# print year

			res[j].append(year) # start date
			res[j].append(year) # end date 
			
			# res[j].append(tempList[j].text)
			#print res[j]," *** 2nd loop for map year attributes"

			urlYearDictionary.append(res[j]) #append the triple to the main dictionary


# print detail_urls
# print urlYearDictionary

output_csv(urlYearDictionary)
