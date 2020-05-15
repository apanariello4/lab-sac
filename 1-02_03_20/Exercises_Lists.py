s1 = ['aba','xyz','aa','x','bbb']
s2 = ['','x','xy','xyx','xx']

def count_pal(s):
    count = 0
    for word in s:
        if (len(word)>=2) and (word[0]==word[-1]):
            count += 1
    return count

print(count_pal(s1))

x1 = ['bbb','ccc','axx','xzz','xaa']

def sort_list(s):
    xlist = []
    alist = []
    for word in s:
        if word[0]=='x':
            xlist.append(word)
        else:
            alist.append(word)

    return sorted(xlist) + sorted(alist)

print(sort_list(x1))