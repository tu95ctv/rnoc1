from test import hinhchunhat, hinhvuong, nothingfrom_test
_='----------------'
class tamgiac():
    pass
class tamgiac1(object):
    pass
def nothing():
    print 'nothing'
tamgiac1_instanse = tamgiac1()
print 'tamgiac1_instanse',tamgiac1_instanse

b= hinhvuong(3)
print b
print b.z
print b.square()
a= tamgiac1()
print 'nothing',nothing
print '---------------'
class DoNothing(object):
    pass
d = DoNothing()
print 'DoNothing',DoNothing
print 'type(d)',type(d)
print _
L = [1, 2, 3]
print 'type(L)',type(L)
print _
print 'type(DoNothing)',type(DoNothing)
print _
print 'type(tuple)',type(tuple)
print 'type(type)',type(type)

print _
def class_factory():
    class Foo(object):
        pass
    return Foo

F = class_factory()
f = F()
print(type(f))
print _
def class_factory1():
    return type('Foo', (), {})

F = class_factory()
f = F()
print(type(f))
print '-------------4--------'
F = type('Foo', (), {})
f = F()
print F
print(type(f))
'''







print '---------- /_\\'
print 'tamgiac:',tamgiac
print 'tamgiac():',tamgiac()
print 'type(tamgiac):',type(tamgiac)

print '---------- /_\\2'
print 'tamgiac1:',tamgiac1
print 'tamgiac1():',tamgiac1()
print 'type(tamgiac1):',type(tamgiac1)
print 'type(a):',type(a)
print '-----------------------'
'''