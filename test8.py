import re
string = 'ExcelImportDoiTac'
rs = re.match('^ExcelImport(.*?)$',string)
print rs.group(1)
