from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GestureSerializer
from .models import Gesture, Post, Photo
from .FingerCountingProject import handtrack
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from multiprocessing import Process
import cv2
import threading
from time import sleep 
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
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def opencam(request):
    cam = VideoCamera()
    return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")

result={}

def transformdata(request):
    list= Gesture.objects.last()
    index= list.name
    color_result= list.moveX + list.moveY
    result= { index: color_result }
    if list.gestureNum==1:
        return render(request,'soowa_web/first.html',{"result": result})
    if list.gestureNum==2:
        return render(request,'soowa_web/first.html',{"result": result})

class GestureListView(viewsets.ModelViewSet):
    queryset = Gesture.objects.all()
    serializer_class = GestureSerializer

def dhand(request):
    #threading.Thread(target=camera).start()
    #sleep(10/100)
    result= handtrack(request)
    #camera(request)
    #p1 = Process(target=camera)
    #p2 = Process(target=handtrack)
    #p1.start()
    #p2.start()
    #p1.join()
    #p2.join()
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
