from django.shortcuts import render

from django.utils import timezone
from django.views.generic.list import ListView

from .models import Advertiser

class AdvertiserListView(ListView):

    model = Advertiser
    context_object_name = 'advertisers'
    template_name = 'ads.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for advertiser in context['advertisers']:
            for ad in advertiser.ads.all():
                ad.incViews() 
        return context
