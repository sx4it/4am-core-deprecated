from jsonrpc import Callable

@Callable
def echo(msg):
    return 'echo ' + msg
