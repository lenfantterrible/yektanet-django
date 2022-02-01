from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.utils import timezone
from django.views.generic.list import ListView
from .models import Advertiser, Ad
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from .forms import AdForm
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

class AdRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        ad.incClicks()
        self.url = ad.link 
        return super().get_redirect_url(*args, **kwargs)

def add_ad(request):
    if request.method == 'POST': 
        form = AdForm(request.POST, request.FILES) 
        if form.is_valid(): 
            ad = Ad()
            ad.name = form.cleaned_data['name']
            ad.advertiser = form.cleaned_data['advertiser']
            ad.link = form.cleaned_data['link']
            ad.img = form.cleaned_data['img']
            ad.save()

            return HttpResponseRedirect('/') 
    else:
        form = AdForm() 

    return render(request, 'add_ad.html', {'form': form})