import zmq, sys
from common import *
from common.jsonrpc import call
import logging
import ast
import api
import inspect

def run():
  """
  Entry point for the Controller function.
  The controller is biding a zmq socket on the port given, it wait for a JsonRPC call.
    .. note::
      for the moment we are reloading the api at each call, this is very bad for perfomance (it increase each call time by 200%)
      but it realy improve the developpement speed on the api component.
  """
  logging.basicConfig(level=logging.DEBUG)
  try:
    port = sys.argv[1]
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    logging.debug("launching " + port)
    socket.bind("tcp://127.0.0.1:" + port)
    while True:
      b = socket.recv()
      # reload each time for testing :)
      reload(api)
      for name in dir(api):
        member = getattr(api, name)
        if inspect.ismodule(member):
          reload(member)

      res = call.processCall(b, api)
      logging.debug(port + "___recv___ >> %s", b)
      logging.debug(port + "___job___ >> %s", res)
      socket.send(res)
  except KeyboardInterrupt:
    logging.debug("ending control" + port)
