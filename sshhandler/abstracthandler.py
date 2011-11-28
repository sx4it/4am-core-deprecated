import zmq

class Handler(object):
	def __init__(self, chan, portlist):
		self.chan = chan
		self.chan.settimeout(None)
		self.to_send = []
		self.str = ""
		self.poll = zmq.core.poll.Poller() # using zmq poll to monitor all socks in reading
		self.poll.register(self.chan, flags=zmq.POLLIN)
	def fileno(self):
		return self.chan.fileno()
	def __call__(self):
		self._send()
		poll = dict(self.poll.poll(timeout=2))
		if self.chan.fileno() in poll.keys():
			self._recv()
		return poll
	def _recv(self):
		s = self.chan.recv(2048)
		if not len(s):
			raise IOError("session finish")
		self.str += s
		split = self.str.split("\r")
		if len(split) > 1:
			self._validate(split[0])
			self.str = ""
			self.str.join(split[1:])
	def _send(self):
		if self.chan.send_ready() and len(self.to_send) > 0:
			for b in self.to_send:
				self.chan.send(b)
			self.to_send = []
	def _validate(self):
		pass
	def shutdown(self):
		self.chan.close()

