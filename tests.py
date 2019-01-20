import socket
import os
import sys
import _pickle as pkl
import statistic as stat
import serv

#WORK_DIRECTORY = r'/sdcard/user/tests/wrkdir'

def saveTest(tst):
    f = open("test.pkl", 'wb')
    pkl.dump(tst, f)
    f.close()

def loadTest():
    if (not os.path.isfile("test.pkl")):
        saveDefaultTest()
    f = open("test.pkl", "rb")
    test = pkl.load(f)
    f.close()
    return test

def saveDefaultTest():
    test = [["std", "qvst1", "answ1"],
            ["std", "qvst2", "answ2"]]
    saveTest(test)

def getQwsts():
    test = loadTest()
    qwsts = []
    for i in test:
        if i[0] == "std":
            qwsts.append(i[1])
    return qwsts

def getAnsws():
    test = loadTest()
    answs = []
    for i in test:
        if i[0] == "std":
            answs.append(i[2])
    return answs

def checkTest(data):
    #print("cT")
    result = data.split("\n")
    name = result.pop(0)
    trAns = getAnsws()
    errs=[]; points =0
    if len(result) != len(trAns):
        raise ValueError;
    for i in range(len(result)):
        if result[i] == trAns[i]:
            points +=1
        else:
            errs.append(i)
    stat.addStatRec((name, points, errs))

def makeTest():
    tfile = open('pages/files/pageHead.html')
    HEAD= tfile.read()
    tfile.close()
    tfile = open('pages/files/pageEnd.html')
    END = tfile.read()
    tfile.close()
    tfile = open('files/task.html')
    TASK = tfile.read()
    tfile.close()

    #f = open('test.t')
    #TODO: choice test
    qwsts = getQwsts()
    print("generating test file")
    html = HEAD
    isQwst = False
    i=0
    for q in qwsts:
        i += 1
        html += TASK.format(qwst=q, i=i)
    html+= END
    #f.close()
    if not os.path.isdir('pages'):
        os.mkdir('pages')
    outf = open("pages/out.html", "w")
    outf.write(html)
    outf.close()

def rewriteTest():
    test = []
    q=''
    print('Welcome to test creator!')
    print('To create a new test input question and true answer to it')
    print('Please input "end" instead the question when test is done')
    while q.lower() != 'end':
        q = input('QUESTION:')
        a = input('ANSWER')
        test.append( ('std', q, a) )
    saveTest(test)
    print('Test saved!')


if __name__=="__main__":
    if 'y' == input('do you want to rewrite test?').lower():
        rewriteTest()
