from django.contrib import admin
from django.urls import include, path
from .views import AdvertiserViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views 

router = DefaultRouter()
router.register(r'advertisers', AdvertiserViewset, basename='Advertiser')

urlpatterns = [
    path('token-auth/', views.obtain_auth_token)
] + router.urls