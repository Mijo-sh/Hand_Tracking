import cv2
import mediapipe as mp
import time
import pyfirmata2

cap=cv2.VideoCapture(0)
while True:
    success,frame=cap.read()
    frame=cv2.flip(frame,1)
 
    cv2.imshow("Hand Tracking",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break