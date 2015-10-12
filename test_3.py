from datetime import datetime
D4_DATETIME_FORMAT = '%H:%M %d/%m/%Y'
d = datetime.strptime('00:20 06/10/2015', D4_DATETIME_FORMAT)
print d