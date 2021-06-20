import cv2
import time
import os
from .HandTrackingModule import handDetector


def handtrack(request):
    # 카메라 화면 출력 사이즈
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    pTime = time.time()

    detector = handDetector(detectionCon=0.75)

    # 손가락 번호: (순서대로) 엄지, 검지, 중지 약지, 소지
    tipIds = [4, 8, 12, 16, 20]


    while True:
        success, img = cap.read()

        # 웹캠 이미지에서 HandTracking
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        fingers = []
        if len(lmList) != 0:
            # 왼손만 사용!!
            # 손가락을 펼치면 fingers 리스트에 1, 펼지지 않으면 fingers 리스트에 0 을 append
            # 엄지
            fingers = []
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 검지, 중지, 약지, 소지
            for id in range(1,5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2] :
                    fingers.append(1)
                else:
                    fingers.append(0)
   
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        cTime = time.time()
        if (cTime-pTime > 2):
            return fingers
