import re
'''
def abc (**kargs):
    print kargs
    
    
#abc(x=2)


import itertools
doi_tac_inputexts = ['lan','ctin','0916022787']
fieldnames= ['Full_name','Don_vi','So_dien_thoai','more']

#dictx = [{'%s'%fieldnames[count]:value} for count,value in enumerate(doi_tac_inputexts)]
#print dictx
dictx = dict(zip(fieldnames,doi_tac_inputexts))
print dictx
dict2 = {'x':1}
abc(**dictx)


a = ['0','1','2','3']
print a.pop()
print a
'''

fieldnames= ['Full_name','Don_vi','So_dien_thoai','more']
sdtfield = fieldnames.pop(2)

a = 'hoang-0300 300403-ctin'
p = re.compile('[\d\s]{3,}')
kq= p.search(a)
std_index = len(re.findall('-',a[:kq.start()]))
fieldnames.insert(std_index, sdtfield)
print fieldnames
#print dir(kq)

'''
x = re.finditer('a(b)(c)','adf abc dsf abc ')
print [m.span() for m in x]
for a in x:
    print tuple(a.groups())
'''
'''
z = [a.start() for a in  m]
print(z)
'''