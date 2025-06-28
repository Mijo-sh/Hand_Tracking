import cv2
import mediapipe as mp
import time
import pyfirmata2

cap=cv2.VideoCapture(0)

hand=mp.solutions.hands
hand_obj=hand.Hands(max_num_hands=1)
drawing=mp.solutions.drawing_utils

while True:
    success,frame=cap.read()
    frame=cv2.flip(frame,1)

    result=hand_obj.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    if result.multi_hand_landmarks:
        hand_keyPoints=result.multi_hand_landmarks[0]
        drawing.draw_landmarks(frame,hand_keyPoints,hand.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break