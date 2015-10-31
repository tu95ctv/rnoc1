class celsius(object):
    print 'adf'
    _temp1=3
    def __init__(self,temperature=0):
        pass
        self.temperature = temperature
        pass
    def get_te(self):
        print 'get...'
        return self._temperature
    def set_te(self,value):
        print "set.."
        if value <-273:
            raise ValueError("temp except")
        
        self._temperature =  value
        #self._temp2 =  value
    temperature =  property()
    temperature = temperature.getter(get_te) #assign object
    temperature = temperature.setter(set_te)
class celsius1(object):
    
    def __init__(self,temperature=0):
        #self.temperature = temperature
        self._temperature = temperature
        pass
    @property
    def temperature(self):
        print 'get...'
        return self._temperature
    @temperature.setter
    def temperature(self,value):
        if value <-273:
            raise ValueError("temp except")
        print "set.."
        self._temperature =  value
        #self._temp2 =  value
    
c =  celsius(-3)
print 'c.temperature assigned in init',c.temperature
print '--2--'
c.temperature=-4
print 'c.temperature', c.temperature

print '---------------decorator-----------'

c =  celsius1(-2325)
print 'c.temperature assigned in init',c.temperature
print '--2--'
c.temperature=-4
print 'c.temperature', c.temperature
