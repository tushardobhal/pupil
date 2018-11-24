from multiprocessing import Pipe, Process
import time
import cv2

from files.world_listener import WorldListener
from files.eye_listener import EyeListener
from files.do_stuff import DoStuff
from files.logger import logger

def main():
    world_dest, world_source = Pipe(duplex=False)
    eye_0_dest, eye_0_source = Pipe(duplex=False)
    eye_1_dest, eye_1_source = Pipe(duplex=False)

    world = WorldListener()
    eye_0 = EyeListener(0)
    eye_1 = EyeListener(1)
    do_stuff = DoStuff()


    world_receiver = Process(target=world.world_receiver, args=(world_source,), name='frame_world')
    eye_0_receiver = Process(target=eye_0.eye_receiver, args=(eye_0_source,), name='gaze_0')
    eye_1_receiver = Process(target=eye_1.eye_receiver, args=(eye_1_source,), name='gaze_1')
    do_some_stuff = Process(target=do_stuff.do_some_stuff, args=(world_dest, eye_0_dest, eye_1_dest), name='do_stuff')

    world_receiver.start()
    eye_0_receiver.start()
    eye_1_receiver.start()
    do_some_stuff.start()

    world_receiver.join()
    eye_0_receiver.join()
    eye_1_receiver.join()
    do_some_stuff.join()

if __name__ == "__main__":
    logger.info("Starting application...")
    main()