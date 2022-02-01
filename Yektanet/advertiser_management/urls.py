from django.urls import include, path
from .views import AdRedirectView, AdvertiserListView, add_ad

urlpatterns = [
    path('', AdvertiserListView.as_view(), name = 'advertiser_list'),
    path('click/<int:pk>/', AdRedirectView.as_view(), name='ad_redirect'),
    path('add_ad/', add_ad, name='add_ad'),

]
