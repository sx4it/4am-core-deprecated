import zmq
 
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")
 
while True:
    print  socket.recv()
    socket.send('received')
