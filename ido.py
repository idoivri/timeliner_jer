import requests
from bs4 import BeautifulSoup

try:
	r = requests.get('http://www.jnul.huji.ac.il/dl/maps/jer/html/date.html')


	print r.status_code

	if r.status_code != 200:
		raise Exception("Status code: %s" % r.status_code)

except Exception, e:
		print "ERROR: %s" % e
		exit()



print '===='

print r.headers['content-type']

print '===='

print r.url

print '===='

#print r.text

soup = BeautifulSoup(r.text)


print '===='



