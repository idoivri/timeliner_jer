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
# Start Date, End Date, Headline, Text,	Media, Media Credit, Media Caption,	Media Thumbnail, Type
def output_csv(mapsDictionary):

    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)

    writer.writerow(('Start Date', 'End Date', 'Headline', 'Text', 'Media', 'Media Credit', 'Media Caption', 'Media Thumbnail'))
    for i in mapsDictionary:
        writer.writerow((i['start'], i['end'], i['headline'], i['text'], i['image'], 'National Library of Israel', i['caption'], i['thumb']))


def get_details(url):
	i = requests.get(url)
	bs = BeautifulSoup(i.text)
	image_url = bs.find('img', {'class':'imgthumb'}).parent.get('href')


	notes = [] ; headline = '' ; text = '' ; caption = ''
	for n in bs.find_all(text="Note"):
		notes.append(n.find_next('td').text)

	if len(notes) == 1:
		headline = notes[0]

	elif len(notes) > 1:
		caption = notes.pop(0)
		headline = notes.pop(0)
		text = '\n'.join(notes)

	return image_url, headline, text, caption


# START HERE

r = requests.get('http://www.jnul.huji.ac.il/dl/maps/jer/html/date.html')

if r.status_code != 200:
	print "Failed to open URL. Status code: %s" % r.status_code
	exit()

soup = BeautifulSoup(r.text)

data = soup.find("table", cols="5")
table = data.find_all('tr')

numCols = 5; #there are 5 columns in the map webpage
alldata = []

for i in range(len(table)):
	row = {}

	if i%2==0:

		# res = [[] for _ in range(numCols)] #create a dictionary of 5 items representing 5 maps: [ [url,year,label] * 5 ]

		#fill in the map URLs:
		tempList = table[i].find_all("td");

		for j in range(numCols):

			img_url = tempList[j].find_next("img").get('src')
			row['thumb'] = img_url

			info_url = 'http://www.jnul.huji.ac.il/dl/maps/jer/html/' + tempList[j].find_next("a").get('href')

			image_url, headline, text, caption = get_details(info_url)

			row['image'] 	= image_url
			row['headline'] = headline.encode('utf-8')
			row['text'] 	= text.encode('utf-8')
			row['caption']	= caption.encode('utf-8')

		#fill in the map year attributes:
		tempList = table[i+1].find_all("td");

		for j in range(numCols):
			y = _extract_year(tempList[j].text)
			year = _year_to_date(y)

			row['start'] = year
			row['end'] = year

			alldata.append(row)

output_csv(alldata)
