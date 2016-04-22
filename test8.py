import re
string = '@ilove@you@very@much@'
kqs=  re.findall(r'@(.*?)@', string)
print kqs