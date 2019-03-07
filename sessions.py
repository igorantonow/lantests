sess = {}

def newSession():
    sid = 0
    while sid in sess:
        sid +=1
    sess[sid] = None
    return sid

def addResult(sid, res):
    sess[sid] = res

def getResult(sid):
    return sess[sid]

def closeSession(sid):
    sess.pop(sid)

if __name__ == "__main__":
    print(sess)
