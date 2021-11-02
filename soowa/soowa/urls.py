
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from soowa_web import views
from soowa_web import FingerCountingProject
from soowa_web import GestureRecognition
from soowa_web import ONEorTWO
from soowa_web import sentence


urlpatterns = [
    url('admin/', admin.site.urls),
    url('opencam', views.opencam, name='opencam'),
    url('dhand', views.dhand, name='dhand'),
    url('GestureRecognition', GestureRecognition.GestureRecognition, name='GestureRecognition'),
    url('oneortwo', ONEorTWO.oneortwo, name='oneortwo'),
    url('new1', views.new1, name='new1'),
    #ㅊㅓㅅ호ㅏ면 
    url('home', views.home, name='home'),
    #문장 1 
    url('next', views.next, name='next'),
    url('sentence3', sentence.sentence3, name='sentence3'),
    
    url(r'^', views.home, name='home'),
    #url(r'^',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
