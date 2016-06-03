import re
strs = 'model = abc \n'
strs2 = 'model = abc,xyz) \n'
str_list = [strs,strs2]
for st in str_list:
    kq = re.search('(model\s*=\s*\S+)\s*\n', st)
    print kq.group(0)
