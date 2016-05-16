x= {'a_main':1,'b_main':2,'c':3,'d':3}
y=['a_main','b_main']
main_dict = {}
for i in y:
    main_dict.update({i:x.pop(i)})
print x
print main_dict