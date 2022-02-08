from django.urls import include, path
from .views import AdRedirectView, AdvertiserListView, AddAdView, StatsView

urlpatterns = [
    path('', AdvertiserListView.as_view(), name = 'advertiser_list'),
    path('click/<int:pk>/', AdRedirectView.as_view(), name='ad_redirect'),
    path('add_ad/', AddAdView.as_view(), name='add_ad'),
    path('stats/', StatsView.as_view(), name='stats'),

]
