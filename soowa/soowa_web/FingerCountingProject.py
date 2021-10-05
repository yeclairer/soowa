import cv2
import time
import os
import threading
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .HandTrackingModule import handDetector


def printcam(request):
    return render(request,'soowa_web/cam.html',{})
  
        
def handtrack(img):  
    cap= cv2.VideoCapture('http://127.0.0.1:8000/opencam')
    pTime = time.time()
    tip = [4, 8, 12, 16, 20]
    state = []
    X = []
    same = 0
    result = -1

    detector = handDetector(detectionCon=0.75)
    
    while True:
        success, img = cap.read()
        # 웹캠 이미지에서 HandTracking
        if not success:
            break
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        fingers = []
        if len(lmList) != 0:
            # 오른손만
            # starsClose
            if lmList[tip[0]][1] > lmList[tip[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 검지, 중지, 약지, 소지
            for id in range(1, 5):
                if lmList[tip[id]][2] < lmList[tip[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        # print(fingers)

        # 0 [0, 0, 0, 0, 0]
        if fingers == [0, 0, 0, 0, 0]:
            if len(state) == 0:
                state.append(0)
            else:
                if state[-1] == 0:
                    same += 1
                else:
                    same = 0
                    state.append(0)

        # 11 [0, 1, 0, 0, 0]
        if fingers == [0, 1, 0, 0, 0]:
            if len(state) == 0:
                state.append(11)
            else:
                if state[-1] == 11:
                    same += 1
                else:
                    same = 0
                    state.append(11)

        # 20 [1, 1, 0, 0, 0]
        if fingers == [1, 1, 0, 0, 0]:
            xThumb = lmList[tip[0]][1]
            yThumb = lmList[tip[0]][2]
            xIndex = lmList[tip[1]][1]
            yIndex = lmList[tip[0]][2]
            xDiff = xThumb - xIndex
            # yDiff = yThumb - yIndex
            if len(X) == 0:
                X.append(200000)
                X.append(xDiff)
            else:
                X.append(xDiff)
     

        # 25 [0, 1, 1, 0, 0]
        if fingers == [0, 1, 1, 0, 0]:
            if len(state) == 0:
                state.append(25)
            else:
                if state[-1] == 25:
                    same += 1
                else:
                    same = 0
                    state.append(25)

        # 30 [1, 1, 1, 0, 0]: 무지개
        if fingers == [1, 1, 1, 0, 0]:
            xThumb = lmList[tip[0]][1]
            if len(X) == 0:
                X.append(300000)
                X.append(xThumb)
            else:
                X.append(xThumb)

        # 32 [1, 1, 0, 0, 1]
        if fingers == [1, 1, 0, 0, 1]:
            if len(state) == 0:
                state.append(32)
                # print(state)
            else:
                if state[-1] == 32:
                    same += 1
                else:
                    same = 0
                    state.append(32)
                    # print(state)

        # 5 [1, 1, 1, 1, 1]
        if fingers == [1, 1, 1, 1, 1]:
            if len(state) == 0:
                state.append(5)
                # print(state)
            else:
                if state[-1] == 5:
                    same += 1
                    # print(same)
                else:
                    same = 0
                    state.append(5)
                    # print(state)

        cTime = time.time()
        if (cTime - pTime > 3):
            if not len(state) == 0:
                if state[-4:] == [0, 5, 0, 5]:
                    state = []
                    #print("star")
                    result = 6
                if state[-2:] == [0, 32]:
                    state = []
                    #print("sun")
                    result = 7
            if len(X) > 5:
                if X[0] == 200000:
                    #print("moon")
                    result = 8
                elif X[0] == 300000:
                    #print("rainbow")
                    result = 9
                X = []
        if result == -1:
            continue

        return result