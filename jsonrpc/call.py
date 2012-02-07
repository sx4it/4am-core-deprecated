#!/usr/bin/env python

import sys
import json
import logging
import traceback

JSON2_SERVER_ERROR_MAX = -32000
JSON2_SERVER_ERROR_MIN = -32099
JSON2_INVALID_REQUEST = -32600
JSON2_METHOD_NOT_FOUND = -32601
JSON2_INVALID_PARAMS = -32602
JSON2_INTERNAL_ERROR = -32603
JSON2_PARSE_ERROR = -32700


class JRPCError(RuntimeError):
    """
    Basic exception class.
    """
    def __init__(self, text):
        RuntimeError.__init__(self, text)

def forgeJRPC(method, requestId, args):
    """
    This function is useful to forge the jsonrpc request on the client side.
    """
    return json.dumps(dict(jsonrpc = '2.0', method = method, params = args, id = requestId))

def analyzeJRPCRes(rawres):
    """
    This function return the result of the jsonrpc answer and raise an
    exception in case of an error.
    """
    resp = json.loads(rawres)
    if resp.get('error') != None:
        raise JRPCError(resp['error'])
    return resp['result']


def invalidRequest(data):
    """
    Forge a jsonrpc invalid request error.
    """
    return dict(code = JSON2_INVALID_REQUEST, message = 'Invalid request.', data = data)

def Callable(func):
    """
    This function is intended to be used as a decorator.
    It flags the method as exportable.
    """
    func.isJRPCCallable = True
    return func

def getCallFunc(RPCRoot, methName):
    """
    This function search beginning at RPCRoot, the methName (a string) and
    return a reference to the function/method.
    """
    current = RPCRoot
    for part in methName.split('.'):
        current = getattr(current, part, None)
        if current is None:
            logging.debug('Method %s not found found.', methName)
            break
    if (current is not None and
            (getattr(current, 'isJRPCCallable', None) is None or
            current.isJRPCCallable is not True)):
    	logging.debug('Method %s found but not set to be exportable.', methName)
        current = None
    return current


def processCall(data, RPCRoot, lookup = getCallFunc):
    """
    The function process a JSON Remote Procedure Call.
    lookup is a method
    """
    error = None
    requestId = None
    try:
        data = json.loads(data)
    except:
        error = dict(code = JSON2_PARSE_ERROR, message = 'Parse error.')
    else:
        jrpcVersion = data.get('jsonrpc')
        method = data.get('method')
        params = data.get('params')
        requestId = data.get('id')
        if jrpcVersion != '2.0':
            error = invalidRequest('Invalid jsonrpc version, only version 2.0 supported.')
        elif not isinstance(method, basestring):
            error = invalidRequest('Method name must be a string.')
        elif not isinstance(params, (list, dict)):
            error = invalidRequest('Params must be an array or an object.')
        elif not isinstance(requestId, (basestring, bool, int, long, float)):
            error = invalidRequest('ID must be a string, a boolean or a number.')
        else:
            if params is None:
                args, kwargs = [], {}
            elif isinstance(params, list):
                args, kwargs = params, {}
            elif isinstance(params, dict):
                args, kwargs = [], params
            else:
                raise RuntimeError

            fun = lookup(RPCRoot, method)
            if fun is None:
                error = dict(code = JSON2_METHOD_NOT_FOUND, message = 'Method not found.')
            else:
                if not kwargs:
                    call = '%s(%s)' % (method, ', '.join(map(repr, args)))
                else:
                    call = '%s(%s)' % (method, ', '.join('%s=%r' % (k,v) for k,v in kwargs.items()))
                logging.debug('Calling %s' % (call,))
                try:
                    result = fun(*args, **kwargs)
                except:
                    e, tb = sys.exc_info()[1:3]
                    if isinstance(e, TypeError) and tb.tb_next is None:
                        error = dict(code = JSON2_INVALID_PARAMS,
                            message = 'Invalid params.',
                            data = dict(python_traceback = traceback.format_exc()))
                    else:
                        error = dict(code = JSON2_INTERNAL_ERROR,
                        	 message = 'Internal error.',
                        	 data = dict(python_traceback = traceback.format_exc()))
    response = dict(jsonrpc = '2.0', id = requestId)
    if error:
        response['error'] = error
    else:
        response['result'] = result
    try:
        response = json.dumps(response)
    except:
        error = dict(code = JSON2_INTERNAL_ERROR, message = 'Internal error.')
        logging.error('Error while building JSON response.')
        response = dict(jsonrpc = '2.0', id = None)
        response = json.dumps(response)
    return response

