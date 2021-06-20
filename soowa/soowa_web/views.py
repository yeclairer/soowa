from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import GestureSerializer
from .models import Gesture, Post, Photo
from .FingerCountingProject import handtrack

# Create your views here.
def first(request):
    return render(request, 'soowa_web/index.html',{})

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

def dhand(request):
    result= handtrack(request)
    finger= sum(result)
    if finger==1:
        return render(request,'soowa_web/index.html', {"result": result} )
    elif finger==2:
        return render(request,'soowa_web/index2.html', {"result": result} ) 
    else:
        return render(request,'soowa_web/index2.html', {"result": result} ) 

class GestureListView(viewsets.ModelViewSet):
    queryset = Gesture.objects.all()
    serializer_class = GestureSerializer

def create(request):
    if(request.method == 'POST'):
        post = Post()
        post.title = request.POST['title']
        post.date = timezone.datetime.now()
        post.save()
        # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
        for img in request.FILES.getlist('imgs'):
            # Photo 객체를 하나 생성한다.
            photo = Photo()
            # 외래키로 현재 생성한 Post의 기본키를 참조한다.
            photo.post = post
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.image = img
            # 데이터베이스에 저장
            photo.save()
        return redirect('/index/' + str(post.id))
    else:
        return render(request, 'soowa_web/index.html')