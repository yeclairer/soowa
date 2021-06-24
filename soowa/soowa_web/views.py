from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GestureSerializer
from .models import Gesture, Post, Photo
from .FingerCountingProject import handtrack,printcam
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from multiprocessing import Process
from .HandTrackingModule import handDetector
import cv2
import threading
import time


# Create your views here.
def first(request):
    return render(request,'soowa_web/first.html',{})

def camera(request):
    return render(request,'soowa_web/cam.html',{})


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        pTime = time.time()
        tip = [4, 8, 12, 16, 20]
        state = []
        X = []
        same = 0
        result=-1
        detector = handDetector(detectionCon=0.75)
        while True:
            success, img = self.video.read()
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
                # Y.append(yDiff)
                # print(X)

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
                        # print(state)ㄴ

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

            #cv2.imshow("Image", img)
            cv2.waitKey(100)

            cTime = time.time()
            if (cTime - pTime > 10):
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
            image = self.frame
            _, jpeg = cv2.imencode('.jpg', image)
            if result == -1:
                return jpeg.tobytes()
            elif result != -1:
                detectresult(result)

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def detectresult(result):
    if result==6:
        return render(request,'soowa_web/index.html', {"result": "별"} ) 
    elif result==7:
        return render(request,'soowa_web/index2.html', {"result": "해"} )     
    elif result==8:
        return render(request,'soowa_web/index3.html', {"result": "달"} ) 
    elif result==9:
        return render(request,'soowa_web/index4.html', {"result": "무지개"} ) 
    else:
        return render(request,'soowa_web/index.html', {"result": "else"} ) 

@gzip.gzip_page
def opencam(request):
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")


result2={}

def transformdata(request):
    list= Gesture.objects.last()
    index= list.name
    color_result= list.moveX + list.moveY
    result= { index: color_result }
    if list.gestureNum==1:
        return render(request,'soowa_web/first.html',{"result": result2})
    if list.gestureNum==2:
        return render(request,'soowa_web/first.html',{"result": result2})

class GestureListView(viewsets.ModelViewSet):
    queryset = Gesture.objects.all()
    serializer_class = GestureSerializer

def dhand(request):
    #threading.Thread(target=camera).start()
    #sleep(10/100)
    result= handtrack(request)
    """
    finger= sum(result)
    if finger==1:
        return render(request,'soowa_web/index.html', {"result": result} )
    elif finger==2:
        return render(request,'soowa_web/index2.html', {"result": result} ) 
    elif finger==3:
        return render(request,'soowa_web/index3.html', {"result": result} ) 
    elif finger==4:
        return render(request,'soowa_web/index4.html', {"result": result} ) 
    """  
    #수정
    if result==6:
        return render(request,'soowa_web/index.html', {"result": "별"} ) 
    elif result==7:
        return render(request,'soowa_web/index2.html', {"result": "해"} )     
    elif result==8:
        return render(request,'soowa_web/index3.html', {"result": "달"} ) 
    elif result==9:
        return render(request,'soowa_web/index4.html', {"result": "무지개"} ) 
    #수정 여기까지

    else:
        return render(request,'soowa_web/index.html', {"result": result} ) 
