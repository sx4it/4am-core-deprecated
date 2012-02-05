"""
help :)
"""
from jsonrpc import call
import logging

@call.Callable
def help():
	""" wooop """
	return "Im helping u."
