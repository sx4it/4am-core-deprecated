"""
test api for autocomplete generation
"""
import jsonrpc


class Test(object):
	""" test class :) """
	class Boh(object):
		""" boh.user class yeah !"""
		@jsonrpc.Callable
		def add(username):
			""" test.add function !"""
			return True
		@jsonrpc.Callable
		def delete(username):
			""" test.delete function !"""
			return True
class Api(object):
	""" API class :) """
	class User(object):
		""" Api.user class yeah !"""
		@jsonrpc.Callable
		def add(username):
			""" api.add function !"""
			return True
		@jsonrpc.Callable
		def delete(username):
			""" api.delete function !"""
			return True
		def deete(username):
			""" api.delete function !"""
			return True
