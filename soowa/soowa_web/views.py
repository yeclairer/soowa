from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GestureSerializer
from .models import Gesture, Post, Photo
from .FingerCountingProject import handtrack,printcam
from .GestureRecognition import GestureRecognition
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from .HandTrackingModule import handDetector
from imutils.video import VideoStream
from imutils.video import FPS
import os,urllib.request,pickle
import imutils
import cv2
import threading
import time
import numpy as np  
from keras.models import model_from_json  
from keras.preprocessing import image  


# Create your views here.
def first(request):
    return render(request,'soowa_web/first.html',{})

def new1(request):
    return render(request,'soowa_web/index_new.html',{})

def new2(request):
    return render(request,'soowa_web/index2_new.html',{})

def camera(request):
    return render(request,'soowa_web/cam.html',{})

#html에 캠띄우기 테스트
def webcam_Test(request):
    return render(request,'soowa_web/webcam_Test.html',{})

class VideoCamera(object):
    def __init__(self):
        #self.video = cv2.VideoCapture(0)
        #(self.grabbed, self.frame) = self.video.read()
        #threading.Thread(target=self.update, args=()).start()
        #8.17 수정
        #initialize the video stream, then allow the camera sensor to warm up
        self.vs = VideoStream(src=0).start()
        # start the FPS throughput estimator
        self.fps = FPS().start()
        
    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=600)
        self.fps.update()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def opencam(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')


def dhand(request):
    result= handtrack(request)
    if result==6:
        return render(request,'soowa_web/index.html', {"result": "별"} ) 
    elif result==7:
        return render(request,'soowa_web/index2.html', {"result": "해"} )     
    elif result==8:
        return render(request,'soowa_web/index3.html', {"result": "달"} ) 
    elif result==9:
        return render(request,'soowa_web/index4.html', {"result": "무지개"} )
    else:
        return render(request,'soowa_web/index.html', {"result": result} ) 

def facesNum(request):
  while (True):
    cascPath = "/Users/yunkyeong/Desktop/project/soowa/soowa_web/templates/soowa_web/haarcascade_frontalface_default.xml"
    i = 0
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    video_capture = cv2.VideoCapture(0)
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=2,
        minSize=(2, 2),
    )
    # print faces found ......
    facesNumber ="Found {0} faces!".format(len(faces))
    return render(request, 'soowa_web/index.html', {'result': facesNumber})

