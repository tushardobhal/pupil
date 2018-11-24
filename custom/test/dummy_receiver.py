import zmq

ctx = zmq.Context()

subscriber = ctx.socket(zmq.SUB)
subscriber.connect("tcp://128.54.244.86:1234")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

print("Connected to ZMQ")

while True:
    msg = subscriber.recv()
    print(msg)