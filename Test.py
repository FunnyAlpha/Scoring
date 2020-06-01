from dateutil import parser

v_time =parser.parse('03.10.2012 00:00:00', dayfirst=True)
print(v_time.month)

print(v_time)