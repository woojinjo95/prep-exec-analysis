import re

s = '2023-08-03T181857F534063+0900'
res = re.sub(r'F\d{6}', '', s)

print(res)