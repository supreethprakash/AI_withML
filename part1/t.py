
words = 'asda@1 asdas333 232ewweq'
s = words.split()
for word in s:
    w = ''.join(e for e in word if e.isalnum())
    print w