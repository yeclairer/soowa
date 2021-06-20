
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from soowa_web import views

router= routers.DefaultRouter()
router.register(r'view',views.GestureListView)

urlpatterns = [
    url('admin/', admin.site.urls),
    url('test/', views.transformdata, name='transformdata'),
    url('test2/', views.dhand, name='dhand'),
    url('home/', views.first, name='first'),
    url('create/', views.create, name='create'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^',include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
