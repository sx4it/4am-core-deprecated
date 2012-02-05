"""
help :)
"""
from jsonrpc import call
import logging

# prendre argument optionel un nom de callable ou de module dont il faudrait recuperer l'aide !

@call.Callable
def help():
	""" wooop """
	return "Im helping u."
