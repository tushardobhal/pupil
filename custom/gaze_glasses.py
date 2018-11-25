from multiprocessing import Process
import time
from multiprocessing.managers import BaseManager

import cv2

from files.world_listener import WorldListener
from files.eye_listener import EyeListener
from files.do_stuff import DoStuff
from files.logger import logger

from files.world import World
from files.pupil import Pupil

def main():
    BaseManager.register('World', World)
    manager_world = BaseManager()
    manager_world.start()
    world_proxy = manager_world.World()

    BaseManager.register('Pupil', Pupil)
    manager_eye_0 = BaseManager()
    manager_eye_0.start()
    eye_0_proxy = manager_eye_0.Pupil()

    BaseManager.register('Pupil', Pupil)
    manager_eye_1 = BaseManager()
    manager_eye_1.start()
    eye_1_proxy = manager_eye_1.Pupil()

    world = WorldListener()
    eye_0 = EyeListener(0)
    eye_1 = EyeListener(1)
    do_stuff = DoStuff()

    world_receiver = Process(target=world.world_receiver, args=(world_proxy,), name='frame_world')
    eye_0_receiver = Process(target=eye_0.eye_receiver, args=(eye_0_proxy,), name='gaze_0')
    eye_1_receiver = Process(target=eye_1.eye_receiver, args=(eye_1_proxy,), name='gaze_1')
    do_some_stuff = Process(target=do_stuff.do_some_stuff, args=(world_proxy, eye_0_proxy, eye_1_proxy), name='do_stuff')

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