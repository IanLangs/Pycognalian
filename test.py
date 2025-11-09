import re
k=re.sub(r'\d', 'd', input("insert a text: "))
k=re.sub(r'[^d\s]+', 'w', k)
k=re.sub(r'\s', 's', k)
print(k)