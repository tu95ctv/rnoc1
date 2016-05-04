from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qs

url = 'http://example.com/?a=text&q2=text2&q3=text3&q2=text4'
u = urlparse(url)
query = parse_qs(u.query)
query.pop('q2', None)
print query
print u
u = u._replace(query=urlencode(query, True))
print u
print(urlunparse(u))