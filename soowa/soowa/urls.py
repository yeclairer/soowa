
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from soowa_web import views
from soowa_web import FingerCountingProject
from soowa_web import GestureRecognition


urlpatterns = [
    url('admin/', admin.site.urls),
    url('opencam', views.opencam, name='opencam'),
    url('facesNum', views.facesNum, name='facesNum'),
    url('camera', views.camera, name='camera'),
    url('dhand', views.dhand, name='dhand'),
    url('webcam_Test', views.webcam_Test, name='webcam_Test'),
    url('GestureRecognition', GestureRecognition.GestureRecognition, name='GestureRecognition'),
    url('new1', views.new1, name='new1'),
    url('new2', views.new2, name='new2'),
    url(r'^', views.first, name='first'),
    #url(r'^',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
