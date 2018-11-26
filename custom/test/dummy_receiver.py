import zmq
import msgpack as serializer

ctx = zmq.Context()

requester = ctx.socket(zmq.REQ)
ip = 'localhost'
port = 50020
requester.connect('tcp://%s:%s'%(ip, port))
requester.send_string('SUB_PORT')
sub_port = requester.recv_string()
print("Connecting to port {}".format(sub_port))

subscriber = ctx.socket(zmq.SUB)
subscriber.connect('tcp://%s:%s'%(ip,sub_port))
subscriber.setsockopt_string(zmq.SUBSCRIBE, 'frame.world')
try:
    while True:
        topic = subscriber.recv_string()
        info = serializer.unpackb(subscriber.recv(), encoding='utf-8')
        # logger.info("Received Topic - {}, Timestamp - {}, Norm_Pos - {}, Confidence - {}".format(topic, info['timestamp'], info['norm_pos'], info['confidence']))
        print(info)
except KeyboardInterrupt:
    requester.close()
    subscriber.close()
    ctx.term()
    raise