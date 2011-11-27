"""
test api for autocomplete generation
"""
from jsonrpc import call


class Test(object):
	""" test class :) """
	class Boh(object):
		""" boh.user class yeah !"""
		@call.Callable
		def add(username):
			""" test.add function !"""
			return True
		@call.Callable
		def delete(username):
			""" test.delete function !"""
			return True

@call.Callable
def add(username):
	""" api.add function !"""
	return True
@call.Callable
def delete(username):
	""" api.delete function !"""
	return "Yeah it is delete !"
