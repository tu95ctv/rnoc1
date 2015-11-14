
def x(self):
    a=2
    print 'adfd'
class a:
    def __init__(self,c):
        self.c = c
    def x(self):
        print self.c
class b(a):
    pass
b_i = b(1)
print id(b_i.__init__),id(b_i)
b_i2 = b(2)
print id(b_i2.__init__),id(b_i2)
print x.__code__
print x.__globals__
print b_i.__self__