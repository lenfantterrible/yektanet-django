from webbrowser import get
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from .models import Advertiser, Ad, Click, View 
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from .forms import AdForm
from django.db.models import Count, F, Sum, Q, Avg

class AdvertiserListView(ListView):

    model = Advertiser
    context_object_name = 'advertisers'
    template_name = 'ads.html'

    def dispatch(self, request, *args, **kwargs):
        self.ip = request.ip
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for advertiser in context['advertisers']:
            for ad in advertiser.ads.all():
                if(ad.approved):
                    ad.inc_views(self.ip)
        return context

class AdRedirectView(RedirectView):

    permanent = False
    query_string = True

    def dispatch(self, request, *args, **kwargs):
        self.ip = request.ip
        return super().dispatch(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        ad.inc_clicks(self.ip)
        self.url = ad.link 
        return super().get_redirect_url(*args, **kwargs)

class AddAdView(FormView):
    template_name = 'add_ad.html' 
    form_class = AdForm 
    success_url = '/'

    def form_valid(self, form):
        Ad.objects.create(name = form.cleaned_data['name'], advertiser = form.cleaned_data['advertiser'], link = form.cleaned_data['link'], img = form.cleaned_data['img'])
        return super().form_valid(form)


class StatsView(TemplateView):

    template_name ='stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        
        context['ads'] = Ad.objects.all()
        context['second_stats'] = Ad.objects.filter(clicks__ip = F('views__ip'), clicks__time__date=F('views__time__date'),  clicks__time__hour=F('views__time__hour')).aggregate(avg=Avg(F('clicks__time') - F('views__time')))
        
        return context
