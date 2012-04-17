'''
remoteExecuter process management
'''

from __future__ import print_function
import sys
import zmq
import subprocess
from common.jsonrpc.zmqProxy import zmqREQServiceProxy

class Proxy(zmqREQServiceProxy):
    '''
    This class is an abstraction of a remoteExecuter process.
    A rE is launched and the class acts as a proxy to contact it.
    '''
    def __init__(self, socketurl):
        '''
        Create a remoteExecuter process.
        FIXME output should maybe be logged instead of written to stdout.
        http://mail.python.org/pipermail/python-list/2008-April/536949.html
        '''
        try:
            self.__proc = subprocess.Popen(['./4am-remoteexecd', socketurl],
                        stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        except:
            print('Unables to create the process, is the PATH correct ?'\
                + str(sys.exc_info()[0]), file=sys.stderr)
            raise
        super(Proxy, self).__init__([socketurl])

    def __del__(self):
        '''
        Destructor, needs to explicitly kill the process to shutdown clearly the
        connections.
        '''
        # BLABLA CLEANING
        super(Proxy, self).__del__()
        self.__proc.kill()
        self.__proc.communicate()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    rE1 = remoteExecuter('tcp://127.0.0.1:5000')
    rE1.getRemoteHostKey('dev2.sx4it.com', 22, 'ssh-rsa')
