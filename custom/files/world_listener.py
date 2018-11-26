import msgpack as serializer
import numpy as np
import zmq

from files.logger import logger


class WorldListener:

    def __init__(self, port_glass_1):
        self.port = port_glass_1

    def world_receiver(self, world_proxy):
        logger.info("Starting World Frames Listener...")
        ctx = zmq.Context()

        requester = ctx.socket(zmq.REQ)
        ip = 'localhost'
        requester.connect('tcp://%s:%s'%(ip, self.port))
        requester.send_string('SUB_PORT')
        sub_port = requester.recv_string()
        logger.info("Connecting to port {}".format(sub_port))

        subscriber = ctx.socket(zmq.SUB)
        subscriber.connect('tcp://%s:%s'%(ip,sub_port))
        subscriber.setsockopt_string(zmq.SUBSCRIBE, 'frame.world')

        try:
            while True:
                topic = subscriber.recv_string()
                info = serializer.unpackb(subscriber.recv(), encoding='utf-8')
                # logger.info("Received Topic - {} Frame - {}, Timestamp - {}".format(topic, info['index'], info['timestamp']))
                frame = []
                while subscriber.get(zmq.RCVMORE):
                    frame.append(subscriber.recv())
                frame_data = np.frombuffer(frame[0], dtype=np.uint8).reshape(info['height'], info['width'], 3)
                world_proxy.set_values(info['index'], frame_data, info['timestamp'])
        except:
            requester.close()
            subscriber.close()
            ctx.term()
            logger.warn('Listener is shut down successfully')
            raise