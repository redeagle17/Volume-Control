import math
import cv2
import mediapipe as mp
import numpy as np
import handTrackModule as htm
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


cap = cv2.VideoCapture(0)
pTime = 0

detector = htm.handDetector()  # Creating the object of handDetector class

# Code from https://github.com/AndreMiras/pycaw
# Below 3 lines are the initialization
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volMin = volume.GetVolumeRange()[0]
volMax = volume.GetVolumeRange()[1]


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)  # lmList has the coordinates of all the points of hand [0...20]
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]  # position of tip of thumb
        x2, y2 = lmList[8][1], lmList[8][2]  # Position of tip of index finger
        cx, cy = (x2 + x1) // 2, (y2 + y1) // 2
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)
        # We have to convert length to volume range
        vol = np.interp(length, [20, 240], [volMin, volMax])
        volBar = np.interp(length, [20, 240], [400, 150])
        volPer = np.interp(length, [20, 240], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (0, 255, 0), 2)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
