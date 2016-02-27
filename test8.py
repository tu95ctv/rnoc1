class A(object):
    create_counter = 0
    def __init__(self):
        A.create_counter +=1
        
a= A()
print a.create_counter
b = A()
print b.create_counter
print A.create_counter