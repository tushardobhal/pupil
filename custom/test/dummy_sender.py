import zmq
import zmq_tools
import time

ctx = zmq.Context()
url = "tcp://128.54.244.86:1234"
publisher= zmq.Socket(ctx, zmq.PUB)
publisher.connect(url)

# publisher = zmq_tools.Msg_Streamer(ctx, url)

# publisher = ctx.socket(zmq.PUB)
# publisher.connect("tcp://127.0.0.1:1234")

while True:
    time.sleep(2)
    publisher.send_string("Hello")