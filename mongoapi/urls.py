from django.urls import path, include
from rest_framework import routers
import mongoapi.views as views
from django.templatetags.static import static

router = routers.DefaultRouter()

router.register(r'mongo', views.MongoViewSet, basename='mongo')

urlpatterns = [
    path('api/', include(router.urls)),
]