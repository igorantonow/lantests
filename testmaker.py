def makefromfile(f):
    tfile = open('files/pageHead.html')
    HEAD= tfile.read()
    tfile.close()
    tfile = open('files/pageEnd.html')
    END = tfile.read()
    tfile.close()
    tfile = open('files/task.html')
    TASK = tfile.read()
    tfile.close()

    html = HEAD
    isQwst = False
    i=0
    for line in f:
        print("log:", 
line)
        if line == "Qwst:\n":
            isQwst = True
            i = i + 1
        elif line == "Answ:\n":
            isQwst=False
        else:
            if isQwst:
                html += TASK.format(qwst=line, i=i)
    html+= END
    return html

f = open("test.t")
g = open('out.html', 'w')
g.write (makefromfile(f))
g.close()
f. close()

