import re

s = '2023-08-03T18:30:04.311116+09:00'
res = re.sub(r'.\d{6}', '', s)

print(res)