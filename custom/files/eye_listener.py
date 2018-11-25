import zmq
import msgpack as serializer

from files.logger import logger

class EyeListener:

    def __init__(self, eye_id):
        self.eye_id = eye_id

    def eye_receiver(self, eye_proxy):
        logger.info("Starting Eye_{} Frames Listener...".format(self.eye_id))

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
        subscriber.setsockopt_string(zmq.SUBSCRIBE, 'gaze.2d.{}'.format(self.eye_id))

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