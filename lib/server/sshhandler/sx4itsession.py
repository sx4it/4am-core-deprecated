import zmq
import abstracthandler
import json

class sx4itsession(abstracthandler.Handler):
  """
  This class is a simple forwarder.
  It store and forward packets to the Controllers. It Use zmq to dynamicly choose between host.
  Distribution between host is equal, it is native in zmq.
  """
  def __init__(self, chan, portlist):
    super(sx4itsession, self).__init__(chan, portlist)
    context = zmq.Context()
    self.sock = context.socket(zmq.REQ)
    for port in portlist:
      self.sock.connect("tcp://127.0.0.1:" + str(port)) #TODO use dynamic IP
    self.poll.register(self.sock, flags=zmq.POLLIN)
  def _validate(self, str):
    self.sock.send(str) # forward to server via zmq
  def __call__(self):
    poll = super(sx4itsession, self).__call__()
    if poll.has_key(self.sock):
      rec = self.sock.recv()
      self.to_send.append(rec)

