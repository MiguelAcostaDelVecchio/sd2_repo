"""
What is the goal of this program?
This program will make the Tello takeoff and go to a height of 10 meters. Afterwards, the drone will move backwards
15 meters, will start recording, and will then go in a circle until the starting point is reached. It will then go
forward 15 meters and land.

Press ESC at any time to make teh Tello land and exit the script

"""

from djitellopy import Tello
import cv2, math, time
from threading import Thread

tello = Tello()
tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    # create a VideoWrite object, recoring to ./video.avi
    height, width, _ = frame_read.frame.shape
    video = cv2.VideoWriter('video2.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

recorder = Thread(target=videoRecorder)
recorder.start()

tello.takeoff()
tello.move_up(50)
tello.flip_back()
tello.flip_forward()
tello.rotate_counter_clockwise(360)
tello.land()

keepRecording = False
recorder.join()
"""
tello.takeoff()



while True:
    # In reality you want to display frames in a separate thread. Otherwise
    #  they will freeze while the drone moves.
    img = frame_read.frame
    cv2.imshow("drone", img)

    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break
    elif key == ord('w'):
        tello.move_forward(30)
    elif key == ord('s'):
        tello.move_back(30)
    elif key == ord('a'):
        tello.move_left(30)
    elif key == ord('d'):
        tello.move_right(30)
    elif key == ord('e'):
        tello.rotate_clockwise(30)
    elif key == ord('q'):
        tello.rotate_counter_clockwise(30)
    elif key == ord('r'):
        tello.move_up(30)
    elif key == ord('f'):
        tello.move_down(30)

tello.land()
"""

