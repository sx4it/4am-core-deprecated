"""
test api for autocomplete generation
"""
from jsonrpc import call
import logging

@call.Callable
def add(param1):
	""" api.add function !"""
	logging.debug("Add -> %s", param1)
	return True
@call.Callable
def delete(param1):
	""" api.delete function !"""
	logging.debug("delete -> %s", param1)
	return "Yeah it is delete !"
@call.Callable
def help():
	""" api.delete function !"""
	return "Yeah it is delete !"
@call.Callable
def deletee(param1):
	""" api.delete function !"""
	logging.debug("delete -> %s", param1)
	return "Yeah it is delete !"
