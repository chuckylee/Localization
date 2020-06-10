string = b'UTS_709_IoT_1 -66 UTS_709_IoT_2 -34 '
s = string.decode()
name = []
value = ""
print(s)
print(len(s))
for x in range(len(s)):
    if s[x] != " ":
        value += s[x]
        # print(s[x])
    else:
        name.append(value)
        value = ""
print(name)
