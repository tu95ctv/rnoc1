import re
p = re.compile('^'+ '(.*?)' +'=(.*?)$',re.VERBOSE)
kq = p.findall('site3g=hc23243')
print kq