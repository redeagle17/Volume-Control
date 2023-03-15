import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

# First step is to initialize the Hands class an store it in a variable
mpHands = mp.solutions.hands

# Now second step is to set the hands function which will hold the landmarks points
hands = mpHands.Hands()

# Last step is to set up the drawing function of hands landmarks on the image
mpDraws = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    # print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape  # (height, width, shape)
                cx, cy = int(lm.x * h), int(lm.y + w)  # converting values to pixels

            mpDraws.draw_landmarks(img, hand,
                                   mpHands.HAND_CONNECTIONS)  # we have passed img because we want to show output on webcam image

    cv2.imshow("Image", img)
    cv2.waitKey(1)
