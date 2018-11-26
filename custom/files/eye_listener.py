import zmq
import msgpack as serializer

from files.logger import logger


class EyeListener:

    def __init__(self, eye_id, port_glass_1):
        self.eye_id = eye_id
        self.port = port_glass_1

    def eye_receiver(self, eye_proxy):
        logger.info("Starting Eye_{} Frames Listener...".format(self.eye_id))

        ctx = zmq.Context()

        requester = ctx.socket(zmq.REQ)
        ip = 'localhost'
        requester.connect('tcp://%s:%s'%(ip, self.port))
        requester.send_string('SUB_PORT')
        sub_port = requester.recv_string()
        logger.info("Connecting to port {}".format(sub_port))

        subscriber = ctx.socket(zmq.SUB)
        subscriber.connect('tcp://%s:%s'%(ip,sub_port))
        subscriber.setsockopt_string(zmq.SUBSCRIBE, 'gaze.3d.{}'.format(self.eye_id))

        try:
            while True:
                topic = subscriber.recv_string()
                info = serializer.unpackb(subscriber.recv(), encoding='utf-8')
                # logger.info("Received Topic - {}, Timestamp - {}, Norm_Pos - {}, Confidence - {}".format(topic, info['timestamp'], info['norm_pos'], info['confidence']))
                eye_proxy.set_values(self.eye_id, info['norm_pos'], info['confidence'], info['timestamp'])
        except KeyboardInterrupt:
            requester.close()
            subscriber.close()
            ctx.term()
            logger.warn('Listener is shut down successfully')
            raise