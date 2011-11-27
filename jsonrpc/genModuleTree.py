#!/usr/bin/env python
import types

def generateModuleTree(root):
	def recGen(root, dic):
		if (type(root) == types.MethodType) and not getattr(root, 'isJRPCCallable', None):
			return
		dic[root.__name__] = {}
		dic = dic[root.__name__]
		dic['__doc__'] = root.__doc__
		for cl in root.__dict__:
			attr = getattr(root, cl)
			if type(attr) == types.TypeType:
				recGen(attr, dic)
			elif type(attr) == types.MethodType:
				recGen(attr, dic)
	dic = {}
	recGen(root, dic)
	return dic

if __name__ == '__main__':
	import testapi
	import json
	import pprint

	dic = generateModuleTree(testapi)
	pprint.pprint(dic)
	open('ModuleTree.json', 'w').write(json.dumps(dic) + "\n") # exporting to a file
