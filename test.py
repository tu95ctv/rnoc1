class hinhchunhat:
    print 'hinhchunhat'

    z=3
    def __init__(self,x,y):
        print 'inside','class hinhchunhat','def __init__(self,x,y):'
        self.x=x
        self.y=y
    def __str__(self):
        return 'self.x %s,self.y %s '%(self.x,self.y)
    def square(self):
        return self.x * self.y
class hinhvuong(hinhchunhat):
    
    print 'hinhvuong'
    def __init__(self,x):
        print 'trong init hinh vuong'
        self.x=x
        self.y =x
class tamgiac():
    print 'tamgiac'
def nothingfrom_test():
    print 'donotthing'
if __name__=="__main__":
    a= hinhvuong(2)
    print a.z
    hinhchunhat.z =4
    print a.z
    
    
