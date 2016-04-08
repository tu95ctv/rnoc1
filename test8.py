a=[1,2,3]
b=[3]
b.extend(a)
b= set(b)
print b
for x in b:
    print x