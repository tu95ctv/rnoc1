'''
cols =[('2',1),('1',2)]
cols.sort(key=lambda x: x[1].creation_counter)
print cols

d ={'MUB_DEFAULT_ROUTER': 26, '3_Carriers': 4, 'Ngay_phat_song_2G': 8}
print d.items()


def getKey(item):
    return item[0]
l = [[2, 3], [6, 7], [3, 34], [24, 64], [1, 43]]
l = sorted(l, key=getKey)
print l

thedict = {'a': 23, 'A': 45}
theset = set(k.lower() for k in thedict)
print theset
print type(theset)

from test8 import Aaa'''
from collections import OrderedDict
base_columns = {'b':2,'a':1,'c':3,'d':2,'e':1,'f':3}
sequence = [x for x in base_columns.iterkeys()]
#sequence =['b','c','d']
bw_sq =  ['b','a']
for x in bw_sq:
    if x in sequence:
        sequence.remove(x)
        
    sequence.append(x)
print 'sequence after bw',sequence
    
#sequence = {'b':2,'a':1,'c':3}
base_columns = {'b':2,'a':1,'c':3,'d':2,'e':1,'f':3}
sequence.extend(['a','b'])
print 'sequence',sequence
base_columns = [(x, base_columns[x]) for x in sequence]

print base_columns