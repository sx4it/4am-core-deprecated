"""
help :)
"""
from jsonrpc import call
import logging
import api

@call.Callable
def help(*param, **dic):
	"""
This is The help module, you can type:
help [modulename].[functionname]
to have a complete information on these function
	"""
	try:
		mod = api
		if dic.get("name") is None:
			if len(param) > 0:
				dic["name"] = param[0]
			else:
				dic["name"] = "help.help"
		for b in dic["name"].split('.'):
			mod = getattr(mod, b)
		return mod.__doc__
	except AttributeError:
		return "Error, no such module : %s. %s"%(dic["name"], help.__doc__)
	return help.__doc__
