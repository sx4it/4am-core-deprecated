import abstracthandler
import zmq
import common.jsonrpc
import json

class shell(abstracthandler.Handler):
  def __init__(self, chan, portlist):
    super(shell, self).__init__(chan, portlist)
    context = zmq.Context()
    self.sock = context.socket(zmq.REQ)
    for port in portlist:
      self.sock.connect("tcp://127.0.0.1:" + str(port)) #TODO use dynamic IP
    self.poll.register(self.sock, flags=zmq.POLLIN)
    self.to_send = ["Hello ! Welcome to sx4it !\n", "$>"]
    print "Inside Shell :)"

  def _recv(self):
    s = self.chan.recv(2048)
    if not len(s):
      raise IOError("session finish")
    if (s == '\177'):
      if len(self.str):
        self.chan.send('\010\033[K')
        self.str = self.str[:-1]
    elif (s == '\004'):
      if not len(self.str):
        raise IOError("session finish")
      else:
        self.str = ""
        self.chan.send("\r\n$>")
    else:
      self.str += s
      self.chan.send(s)
    split = self.str.split("\r")
    if len(split) > 1:
      if not self._validate(split[0]):
        raise IOError("session finish")
      self.str = ""
      self.str.join(split[1:])

  def _send(self):
    if self.chan.send_ready() and len(self.to_send) > 0:
      for b in self.to_send:
        self.chan.send(b.replace('\n', '\r\n'))
      self.to_send = []

  def _validate(self, _str):
    print "WTF"
    _str = _str.split()
    if not len(_str) :
      self.to_send.append("\n$>")
      return True
    if (_str[0] == "exit"):
      return False

    if (_str[0].find('.') < 0):
      _str[0] += '.' + _str[0]

    send = jsonrpc.call.forgeJRPC(_str[0], 'jsonrpc', _str[1:])
    self.sock.send(send)
    res = self.sock.recv()
    
#    self.to_send.append("\r\nrecv < fun<" + _str[0] + ">" + repr(_str[1:]) + ">\r\n" + "$>")
#    self.to_send.append("\r\nsending : \r\n" + send + "\r\n$>")
    try:
      self.to_send.append("\n" + jsonrpc.call.analyzeJRPCRes(res) + "\n$>")
    except jsonrpc.call.JRPCError as error:
      self.to_send.append("\n" + json.loads(str(res))['error']["message"] + "\n$>")
    except :
      self.to_send.append("\n" +  "error" + "\n")
    return True
    #TODO prompt a shell for the user. and forward when ready json to server

