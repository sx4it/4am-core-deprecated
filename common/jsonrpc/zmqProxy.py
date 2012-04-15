import zmq
from proxy import Proxy
import call

class zmqREQServiceProxy(Proxy):
    """
    Basic JSONRPC Proxy using zmq.
    This class inherit of the jsonrpc proxy and define the __call__ method forwarding the request to.
    """
    def __init__(self, serviceURLs, zmqContext=None):
        self.__serviceURLs = serviceURLs
        self.__context = zmqContext or zmq.core.context.Context.instance()
        self.__socket = self.__context.socket(zmq.REQ)
        for serv in serviceURLs:
            self.__socket.connect(serv)
        super(zmqREQServiceProxy, self).__init__()

    def __call__(self, *args, **kwargs):
        postdata = super(zmqREQServiceProxy, self).__call__(*args, **kwargs)
        self.__socket.send(postdata)
        return call.analyzeJRPCRes(self.__socket.recv())

    def __del__(self):
        '''
        This is not mandatory, the socket would be garbage collected.
        '''
        self.__socket.close()
