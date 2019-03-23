import socket
import os
import sys
import _pickle as pkl
import random
import statistic as stat
import serv
import sessions

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
    sessID = result.pop(0)
    trAns = getAnsws()
    errs=[]; points =0
    if len(result) != len(trAns):
        raise ValueError;
    for i in range(len(result)):
        if result[i] == trAns[i]:
            points +=1
        else:
            errs.append(i)
    stat.addStatRec((name, points, errs, sessID))
    print(name, sessID, points, errs);

def makeTest():
    tfile = open('pages/files/pageHead.html', encoding='utf-8')
    HEAD= tfile.read()
    tfile.close()
    tfile = open('pages/files/pageEnd.html', encoding='utf-8')
    END = tfile.read()
    tfile.close()
    tfile = open('pages/files/task.html', encoding='utf-8')
    TASK = tfile.read()
    tfile.close()

    #TODO: choice test
    qwsts = getQwsts()
    print("generating test file")
    sessionID = sessions.newSession()
    html = HEAD.replace('{sessID}', str(1))
    l = list(range(len(qwsts)))
    random.shuffle(l)
    fnum=0
    for i in l:
        fnum+=1
        q = qwsts[i]
        html += TASK.format(qwst=q, i=i, fnum=fnum)
    html+= END
    #f.close()
    if not os.path.isdir('pages'):
        os.mkdir('pages')
    outf = open("pages/out.html", "w", encoding='utf-8')
    outf.write(html)
    outf.close()

def rewriteTest():
    test = []
    q=''
    print('Welcome to test creator!')
    print('To create a new test input question and true answer to it')
    print('Please input "end" instead the question when test is done')
    q = input('QUESTION:')
    while q.lower() != 'end':
        a = input('ANSWER: ')
        test.append( ('std', q, a) )
        q = input('QUESTION: ')
    saveTest(test)
    print('Test saved!')


if __name__=="__main__":
    if 'y' == input('do you want to rewrite test?(y/n)').lower():
        rewriteTest()
