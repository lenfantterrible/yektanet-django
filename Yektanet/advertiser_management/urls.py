from django.urls import include, path
from .views import AdvertiserListView

urlpatterns = [
    path('', AdvertiserListView.as_view(), name = 'advertiser_list'),
]
