import collections

print 'Regular dictionary:'
d =  {'site_name_1':'SN1', 'site_name_2':'SN2','site_ID_2G':'2G', 'site_id_3g':'3G'}

for k, v in d.items():
    print k, v

print '\nOrderedDict:'
d = collections.OrderedDict()
d= {'site_name_1':'SN1', 'site_name_2':'SN2','site_ID_2G':'2G', 'site_id_3g':'3G'}
for k, v in d.items():
    print k, v
    