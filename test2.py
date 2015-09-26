import re
string = 'amos [site_id_3g] hello [RNC] [site_id_3g]'
p = re.compile('\[(.+?)(\])')
kqsearch = p.search(string)
#kqs = re.findall('\[(.+?)(\])', string)
kqs = p.findall(string)
print kqsearch.lastindex
print dir(kqsearch)
print 'kqs',kqs

for attr in dir(kqsearch):
    print "obj.%s = %s" % (attr, getattr(kqsearch, attr))