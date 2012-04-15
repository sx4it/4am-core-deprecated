#!/usr/bin/env python

import zmq
import json
import logging
import call

class Proxy(object):
  """
  """
  def __init__(self):
    self.__callMeth = ""
  def __getattr__(self, name):
    if self.__callMeth != '':
        self.__callMeth += '.'
    self.__callMeth += name
    return self
  def __call__(self, *args, **kwargs):
    if args and kwargs:
      raise RuntimeError('You cannot use both non-keyword arguments and keyword arguments at the same time.')
    postdata = call.forgeJRPC(self.__callMeth, 'jsonrpc', args or kwargs)
    self.__callMeth = ""
    logging.debug('forged JRPC is : %s', postdata)
    return postdata

