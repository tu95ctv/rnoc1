
def x(self):
    a=2
    print 'adfd'
class A:
    d=[]
    def __init__(self):
        self.c = 'a'
    def x(self):
        print self.c
class B(A):
    pass
print A.d,B.d,id(A.d),id(B.d)
B.d.append(1)
print A.d,B.d,id(A.d),id(B.d)
ia=A()
ib=B()
print ia.d,ib.d,id(ia.d),id(ib.d)
ib.d.append(1)
print ia.d,ib.d,id(ia.d),id(ib.d)