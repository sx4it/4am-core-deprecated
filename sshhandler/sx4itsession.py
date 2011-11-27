import zmq
import abstracthandler

class sx4itsession(abstracthandler.Handler):
	def __init__(self, chan, portlist):
		super(sx4itsession, self).__init__(chan, portlist)
		context = zmq.Context()
		self.sock = context.socket(zmq.REQ)
		for port in portlist:
			self.sock.connect("tcp://127.0.0.1:" + str(port))
		self.poll.register(self.sock, flags=zmq.POLLIN)
	def _validate(self, str):
		self.sock.send(str) # forward to server via zmq
	def __call__(self):
		poll = super(sx4itsession, self).__call__()
		if poll.has_key(self.sock):
			recv = self.sock.recv()
			self.to_send.append(recv)

