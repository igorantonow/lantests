import socket
import os
import sys
import _pickle as pkl
import serv

def addStatRec(record):
    if (not os.path.isfile("stat.pkl")):
        f = open("stat.pkl", "wb")
        pkl.dump(["format=my"], f)
        f.close()
    f = open("stat.pkl", "rb")
    recs = pkl.load(f)
    f.close()
    f = open("stat.pkl", "wb")
    recs.append(record)
    pkl.dump(recs, f)
    f.close()

def loadStat():
    if (not os.path.isfile("stat.pkl")):
        f = open("stat.pkl", "wb")
        pkl.dump(["format=my"], f)
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
    raise ValueError("cannot find records about "+name)

def oformResTest(name):
    res = getLastTestRes(name)
    mistakes = [ i+1 for i in res[2] ]
    text = "Congratulations! You have "+\
           str(res[1]*100//len(serv.getAnsws()))+\
           "% correct answers. Your mistakes:"+\
           str(mistakes)
    return text.encode("utf-8")

