import msgpack as serializer
import numpy as np
import zmq
from multiprocessing import Queue

from files.world import World
from files.logger import logger

class WorldListener:

    def __init__(self):
        pass

    def world_receiver(self, world_source):
        logger.info("Starting World Frames Listener...")
        ctx = zmq.Context()

        requester = ctx.socket(zmq.REQ)
        ip = 'localhost'
        port = 50020
        requester.connect('tcp://%s:%s'%(ip, port))
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
                world = World(info['index'], info['timestamp'], frame_data)
                world_source.send(world)
                # cv2.imshow('frame.world', frame_data)
                # cv2.waitKey(1)
        except:
            requester.close()
            subscriber.close()
            ctx.term()
            world_source.close()
            logger.warn('Listener is shut down successfully')