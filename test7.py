'''
cols =[('2',1),('1',2)]
cols.sort(key=lambda x: x[1].creation_counter)
print cols
'''
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