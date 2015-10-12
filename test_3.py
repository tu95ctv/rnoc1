class Employee:
    'Common base class for all employees'
    empCount = 0
    
    def __init__(self, name, salary):
       self.name = name
       self.salary = salary
       Employee.empCount += 1
    
    def displayCount(self):
      print "Total Employee %d" % Employee.empCount
    
    def displayEmployee(self):
       print "Name : ", self.name,  ", Salary: ", self.salary
x=100
s="abc"
def change(x):
    x +=1
def changes(x):
    x +='d'
def changeo(x):
    x.salary +=1
       
a = Employee('tu',100)
print a.empCount
b = Employee('ta',100)
print a.empCount


    
change (x)
print x
changes (s)
print s
changeo(a)
print a.salary