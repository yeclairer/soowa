from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GestureSerializer
from .models import Gesture, Post, Photo
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
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

def home(request):
    return render(request,'soowa_web/home.html',{})

def train1(request):
    return render(request,'soowa_web/train1.html',{})

def train2(request):
    return render(request,'soowa_web/train2.html',{})

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
