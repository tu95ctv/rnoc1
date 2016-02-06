class DBInterfaceMeta(type):
    # we use __init__ rather than __new__ here because we want
    # to modify attributes of the class *after* they have been
    # created
    def __new__(cls, name, bases, dct):
        if  'registry' not in dct:
            # this is the base class.  Create an empty registry
            if name == 'DBInterface':
                dct['registry'] = {'DBInterface':1}
            else:
                dct['registry'] = {}
                print name
        else:
            # this is a derived class.  Add cls to the registry
            interface_id = name.lower()
            print interface_id,'da co attr registry'
            dct['registry'][interface_id]  = cls
            
        return super(DBInterfaceMeta, cls).__new__(cls,name, bases, dct)
        
class DBInterface(object):
    __metaclass__ = DBInterfaceMeta
    
print(DBInterface.registry)

class FirstInterface(DBInterface):
    pass

class SecondInterface(DBInterface):
    pass

class SecondInterfaceModified(SecondInterface):
    pass

print(DBInterface.registry)