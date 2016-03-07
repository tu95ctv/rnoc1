import xlsxwriter

workbook = xlsxwriter.Workbook('BCN_04032016.xlsx')

worksheet = workbook.add_worksheet('abcd')
chart = workbook.add_chart({'type': 'pie'})

data = [
    ['Pass', 'Fail','mid'],
    [60, 20,30],
]

worksheet.write_column('A1', data[0])
worksheet.write_column('B1', data[1])

chart.add_series({
    'categories': '=Sheet1!$A$1:$A$3',
    'values':     '=Sheet1!$B$1:$B$3',
    'points': [
        {'fill': {'color': 'green'}},
        {'fill': {'color': 'red'}},
        {'fill': {'color': 'yellow'}},
    ],
})

worksheet.insert_chart('C3', chart)

workbook.close()