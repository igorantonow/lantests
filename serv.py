import socket
import os
import sys
import _pickle as pkl
import statistic as stat
import tests

WORK_DIRECTORY = r'/sdcard/user/tests/wrkdir'

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
      tests.checkTest(content)
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
      tests.makeTest()
      file='out.html'
  if file.count("getLastTestRes")>0:
      #content = str(getLastTestRes(file.split("=")[1]))
      #content = content.encode('utf-8')
      content = stat.oformResTest(file.split("=")[1])
  else:
      content = None
  
  print('Sending file:', file)
  try:
    if content==None:
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


'''========CODE========='''
def run():
	os.chdir(WORK_DIRECTORY)
	
	print(tests.getQwsts())
	print(stat.getLastTestRes('Name'))
	
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
	
if __name__=="__main__":
    run()
