import six
MyClass = type('MyClass', (), {})
print type(MyClass)
thumuc={'tmp.txt':1,'foo.txt':2}
class base(object):
    someattr = 'someattr'
class InterfaceMeta(type):
    def __new__(cls, name, parents, dct):
        # create a class_id if it's not specified
        print 'name',name,type(name)
        dct[name]='Interface'
        if 'class_id' not in dct:
            dct['class_id'] = name.lower()
        
        # open the specified file for writing
        if 'file' in dct:
            filename = dct['file']
            dct['file'] = thumuc[filename]
        
        # we need to call type.__new__ to complete the initialization
        return super(InterfaceMeta, cls).__new__(cls, name, parents, dct)
    
Interface = InterfaceMeta('Interface_dung type', (), dict(file='tmp.txt'))
print type(Interface)
print(Interface.class_id)
print(Interface.file)
print (Interface.__name__)
class Interface():
    __metaclass__ = InterfaceMeta
    file = 'tmp.txt'
    def somefunc(self):
        return 1
    print 'In Interface'
print Interface.__name__    
print(Interface.class_id)
print(Interface.file)
print 'type(Interface)',type(Interface)
#print(Interface.someattr)
print 'dir(Interface)',dir(Interface)
print Interface.__dict__
print'---------------'


class UserInterface(Interface):
    file = 'foo.txt'
print 'UserInterface.Interface',UserInterface.Interface
print 'UserInterface.UserInterface',  UserInterface.UserInterface    
print(UserInterface.file)
print('UserInterface.class_id',UserInterface.class_id)
print 'type(UserInterface)',type(UserInterface)
#print(UserInterface.someattr)
print'--------six-------'
class Form1(six.with_metaclass(InterfaceMeta,base)):
    pass
class Form(base):
    __metaclass__ = InterfaceMeta
class UserInterfacesix(Form):
    file = 'foo.txt'
print(UserInterfacesix.file)
print(UserInterfacesix.class_id)
print 'type(UserInterface)',type(UserInterfacesix)
print UserInterfacesix.someattr















print'------------init-------'
class DBInterfaceMeta(type):
    # we use __init__ rather than __new__ here because we want
    # to modify attributes of the class *after* they have been
    # created
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            # this is the base class.  Create an empty registry
            #dct['tu'] = 'tu'
            cls.tu = 'tu'
            cls.registry = {}
        else:
            # this is a derived class.  Add cls to the registry
            interface_id = name.lower()
            cls.registry[interface_id] = cls
            
        super(DBInterfaceMeta, cls).__init__(name, bases, dct)
        
class DBInterface(object):
    __metaclass__ = DBInterfaceMeta
    
print(DBInterface.registry)
print DBInterface.tu

class FirstInterface(DBInterface):
    pass

class SecondInterface(DBInterface):
    pass

class SecondInterfaceModified(SecondInterface):
    pass

print(DBInterface.registry)
print(FirstInterface.registry)