﻿import socket
import os
import sys
import _pickle as pkl
import serv
import tests

def addStatRec(record):
    if (not os.path.isfile("stat.pkl")):
        f = open("stat.pkl", "wb")
        pkl.dump([("fict", 10, [3,4])], f)
        f.close()
    f = open("stat.pkl", "rb")
    recs = pkl.load(f)
    f.close()
    f = open("stat.pkl", "wb")
    recs.append(record)
    pkl.dump(recs, f)
    f.close()
    createStatPage()

def loadStat():
    if (not os.path.isfile("stat.pkl")):
        f = open("stat.pkl", "wb")
        pkl.dump([("fict", 10, [3,4])], f)
        f.close()
    f = open("stat.pkl", "rb")
    stat = pkl.load(f)
    f.close()
    return stat

def getLastTestRes(name):
    print("getLastTestRes("+name+')')
    stat = loadStat()
    stat.reverse()
    for record in stat:
        if record[0] == name:
            return record
    return ('err', -1, [-2])
    #raise ValueError("cannot find records about "+name)

def oformResTest(name):
    res = getLastTestRes(name)
    if res[1] < 0:
        return 'вы можете найти результаты по ссылке:'.encode('utf-8')
    mistakes = [ i+1 for i in res[2] ]
    #text = "Congratulations! You have "+\
    #       str(res[1]*100//len(tests.getAnsws()))+\
    #       "% correct answers. Your mistakes:"+\
    #       str(mistakes)
    text = "Поздравляем! У Вас " +\
             str(res[1]*100//len(tests.getAnsws()))+\
             "% ответов верные."# Ваши ошибки:"+\
    #         str(mistakes)
    #TODO: indicate mistakes
    return text.encode("utf-8")

def _printStat():
    stat = loadStat()
    for i in stat:
        print(i)

def createStatPage():
    f = open("pages/files/stat.html", encoding='utf-8')
    html = f.read()
    f.close()
    f = open("pages/files/statItem.html", encoding='utf-8')
    item = f.read()
    f. close()
    table = ""
    for i in loadStat():
        mistakes = str([j+1 for j in i[2]])
        tr = item.format(name=i[0], right=i[1], wrong=mistakes)
        table += tr
    html = html.format(table = table)
    if not os.path.isdir('pages'):
        os.mkdir('pages')
    f = open("pages/stat.html", "w", encoding='utf-8')
    f.write(html)
    f.close()

if __name__=="__main__":
    _printStat()
    createStatPage()
