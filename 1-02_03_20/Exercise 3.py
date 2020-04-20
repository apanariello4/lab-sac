def string(s):
    if len(s) > 4:
        return s[:2]+s[-2:]
    else:
        return ""

s1 = "Hello World"
s2 = "Ciao"
print(string(s1))
print(string(s2))

def string_star(s):
    if len(s) > 4:
        return s.replace(s[2:-2], '*' * (len(s)-4))
    else:
        return ""

print(string_star(s1))