import re
import requests
from bs4 import BeautifulSoup


# helper function to extract year string from year
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


r = requests.get('http://www.jnul.huji.ac.il/dl/maps/jer/html/date.html')

""" try:
	r = requests.get('http://www.jnul.huji.ac.il/dl/maps/jer/html/date.html')


	print r.status_code

	if r.status_code != 200:
		raise Exception("Status code: %s" % r.status_code)

except Exception, e:
		print "ERROR: %s" % e
		exit()"""




soup = BeautifulSoup(r.text)


#print '===='

data = soup.find("table", cols="5")

#print data

table = data.find_all('tr')

numCols = 5; #there are 5 columns in the map webpage

urlYearDictionary = [] #dictionary to contain url,year,label triples

#print "length is:"+str(len(table))

for i in range(len(table)):

	if i%2==0:

		res = [[] for _ in range(numCols)] #create a dictionary of 5 items representing 5 maps: [ [url,year,label] * 5 ]

		#fill in the map URLs:
		tempList = table[i].find_all("td");

		for j in range(numCols):

			res[j].append(tempList[j].find_next("img").get('src'))
			#print res[j]," *** 1st loop for map links"

		#fill in the map year attributes:
		tempList = table[i+1].find_all("td");

		for j in range(numCols):
			res[j].append(_extract_year(tempList[j].text))
			res[j].append(tempList[j].text)
			#print res[j]," *** 2nd loop for map year attributes"

			urlYearDictionary.append(res[j]) #append the triple to the main dictionary



print urlYearDictionary












