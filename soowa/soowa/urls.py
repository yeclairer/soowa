
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from soowa_web import views
from soowa_web import sentence


urlpatterns = [
    url('admin/', admin.site.urls),
    url('opencam', views.opencam, name='opencam'),
    url('new1', views.new1, name='new1'),
    #ㅊㅓㅅ호ㅏ면 
    url('home', views.home, name='home'),

    url('train1', views.train1, name='train1'),
    url('train2', views.train2, name='train2'),
    url('sentence0', sentence.sentence0, name='sentence0'),
    url('sentence1', sentence.sentence1, name='sentence1'),
    url('sentence2', sentence.sentence2, name='sentence2'),
    url(r'^', views.home, name='home'),
    #url(r'^',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
