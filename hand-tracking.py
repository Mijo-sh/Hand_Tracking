import cv2
import mediapipe as mp
import time
import pyfirmata2
import math

def get_angle(p1,p2):
    dx=p2.x-p1.x
    dy=p2.y-p1.y
    return math.degrees(math.atan2(dy,dx))

def is_finger_extended(lm,tip_id,pip_id,wrist_id=0,factor=0.05):
    tip_y=lm[tip_id].y
    pip_y=lm[pip_id].y
    wrist_y=lm[wrist_id].y
    threshold=abs(wrist_y-pip_y)*factor
    return(pip_y-tip_y)>threshold

def handDirection(lst):
    lm=lst.landmark

    fingers_extended=[
        is_finger_extended(lm, 8, 6),
        is_finger_extended(lm, 12, 10),
        is_finger_extended(lm, 16, 14),
        is_finger_extended(lm, 20, 18) ]

    all_extended=all(fingers_extended)
    all_folded=not any(fingers_extended)

    thumb_angle=get_angle(lm[2],lm[4])
    if -135<thumb_angle<-45:
        thumb_dir="up"
    elif 45<thumb_angle<135:
        thumb_dir="down"
    else:
        thumb_dir="side"

    hand_dir="right" if lm[20].x>lm[5].x else "left"

    if all_folded and thumb_dir in ["up","down"]:
        return thumb_dir
    elif all_extended and thumb_dir in ["up","down"]:
        return f"{thumb_dir}-{hand_dir}"
    elif all_extended:
        return hand_dir

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

        diff_y=abs(hand_keyPoints.landmark[0].y-hand_keyPoints.landmark[8].y)
        diff_x=abs(hand_keyPoints.landmark[0].x-hand_keyPoints.landmark[8].x)
        if diff_y<diff_x:
            direction=handDirection(hand_keyPoints)
            moveServo(direction)
            if direction=='right':
                print('right')
            elif direction=='left':
                print('left')
            elif direction=='up':
                print('up')
            elif direction=='down':
                print('down')
            elif direction=='up-right':
                print('up-right')
            elif direction=='down-right':
                print('down-right')
            elif direction=='up-left':
                print('up-left')
            elif direction=='down-left':
                print('down-left')

    cv2.imshow("Hand Tracking",frame)
    if cv2.waitKey(1)&0xFF==ord('q'):
        cv2.destroyAllWindows()
        cap.release()
        break