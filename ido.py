import requests

r = requests.get('http://www.jnul.huji.ac.il/dl/maps/jer/html/date.html')

print r.status_code

print '===='

print r.headers['content-type']
