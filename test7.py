import re
string = "RXOTG-89, RXOTG-289"
rs = re.findall('RXOTG-(\d+)',string)
print rs
