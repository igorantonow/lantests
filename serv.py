import socket
import os
import sys
import _pickle as pkl

WORK_DIRECTORY = r'/sdcard/user/serv/tests/wrkdir'

#-----statistics operating-----
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


#-------test operating---------
def saveTest(tst):
    f = open("test.pkl", 'wb')
    pkl.dump(tst, f)

def loadTest():
    if (not os.path.isfile("test.pkl")):
        saveDefaultTest()
    f = open("test.pkl", "rb")
    return pkl.load(f)

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
    print("cT")
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
    addStatRec((name, points, errs))

def makeTest():
    tfile = open('files/pageHead.html')
    HEAD= tfile.read()
    tfile.close()
    tfile = open('files/pageEnd.html')
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

    outf = open("out.html", "w")
    outf.write(html)
    outf.close()

#-------net operating----------

def loadcontent(file):
    '''
    finds file and returns byte-like object

    finds file or if its directory, finds
    'index.html' in this directory.
    if file does not exist, throws exceprion
    '''
    os.chdir(WORK_DIRECTORY)
    if os.path.isfile(file):
        fi=open(file, 'rb')
    else:
        try:
            path=os.path.join(file, 'index.html')
            fi=open(path, 'rb')
        except Exception as e:
            raise e
    cont=fi.read()
    fi.close()
    return cont

def getData(sock):
  '''returns decoded data from SOCK socket'''
  data=sock.recv(1024)
  '''
  while True:
    newData=sock.recv(1)
    if not newData:
      break
    print(newData)
    data = data + newData
  '''

  return data.decode('utf-8')


def createAnsw(ddata):
  '''
  parses decoded data and returns byte-like answer

  parses data, finds file and makes answer.
  '''
  BAD_REQW='HTTP/1.1 502 BAD REQUEST'

#  ddata=data.decode('utf-8')
  if ddata.isspace():
    print('data is empty')
    ans=BAD_REQW
    reqv=ans.encode('utf-8')
    return reqv

  '''here <processing> different HTTP ACTIONS'''
  HTTPAction = ddata.split(None, 1)[0] #bug! index out of range (on test.t) 

  if HTTPAction.upper() == 'POST':
    #sprint(ddata)
    directory = ddata.split(None,2)[1]
    content = ddata.split("\r\n\r\n",1)[1]
    print((directory, content))

    if (directory=='/resTest.py'):
      checkTest(content)
    ans = "HTTP/1.1 200 OK"
    return ans.encode('utf-8')

  elif HTTPAction.upper() != 'GET':
    print("action isn't a2aliable!")
    print(ddata)
    ans=BAD_REQW
    reqv=ans.encode('utf-8')
    return reqv

  file=ddata.partition(' HTTP/1.1')[0][5:]

  if file == 'test.py':
      makeTest()
      file='out.html'

  print('Sending file:', file)
  try:
    content=loadcontent(file)
  except FileNotFoundError as e:
    print(e)
    ans='''HTTP/1.1 404 NOT FOUND'''
    reqv=ans.encode('utf-8')
  else:
    ans='''HTTP/1.1 200 OK
charset: utf-8
Content-type: text/html;'''
   #TODO: get really content type
    ans+='''
Content-Length: '''+str(len(content)) + \
   '''
Content-Language: ru
connection: close

'''
    reqv = ans.encode('utf-8') + content
  return reqv


'''=====DIFFERENCE PART FOR TESTING======'''

def resTest(cont):
    print('---TEST RES---')
    answs = cont.split('\n')
    for i in answs:
       print(i)
    name = answs.pop(0)
    #res = checkTest(answs)

'''========CODE========='''

os.chdir(WORK_DIRECTORY)

print(getQwsts())

sock = socket.socket()
sock.bind(('', 8080))

while True:
  print("server is working")
  sock.listen(2)
  conn, addr = sock.accept()

  print ('connected:', addr)


  #data = conn.recv(1024)
  #ddata=data.decode('utf-8')

  ddata = getData(conn)
  #warning: next expression isn't good
  if 0 <= ddata.find('exit'):
    print('exit')
    conn.close()
    break
  ans = createAnsw(ddata)
  conn.sendall(ans)

  print('page send, conn resetting...')
  print('_____________')
  conn.close()

print('server closed')
