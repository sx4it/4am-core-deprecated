"""
help :)
"""
from jsonrpc import call
import logging
import api

@call.Callable
def help(name="help.help"):
	"""
This is The help module, you can type:
help [modulename].[functionname]
to have a complete information on these function
	"""
	try:
		mod = api
		for b in name.split('.'):
			mod = getattr(mod, b)
		return mod.__doc__
	except AttributeError:
		return "Error, no such module : %s. %s"%(name, help.__doc__)
	return help.__doc__
