default = {4:'lam'}
kwarg = {1:'anh',2:'yeu',3:'em'}
l =list(kwarg)
print l
del kwarg[1]
print kwarg
default.update(kwarg)
print default