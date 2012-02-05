import abstracthandler

class shell(abstracthandler.Handler):
	def __init__(self, chan, portlist):
		super(shell, self).__init__(chan, portlist)
		self.to_send = ["Hello ! Welcome to sx4it !\r\n", "$>"]
		print "Inside Shell :)"
	def _validate(self, str):
		self.to_send.append("recv <" + str + ">\r\n" + "$>")
		#TODO prompt a shell for the user. and forward when ready json to server

