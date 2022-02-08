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
from django.db.models import Count, F, Sum

class AdvertiserListView(ListView):

    model = Advertiser
    context_object_name = 'advertisers'
    template_name = 'ads.html'

    def dispatch(self, request, *args, **kwargs):
        self.ip = get_client_ip(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for advertiser in context['advertisers']:
            for ad in advertiser.ads.all():
                if(ad.approved):
                    View.objects.create(ad=ad, ip=self.ip)
        return context

class AdRedirectView(RedirectView):

    permanent = False
    query_string = True

    def dispatch(self, request, *args, **kwargs):
        self.ip = get_client_ip(request)
        return super().dispatch(request, *args, **kwargs)
    
    def get_redirect_url(self, *args, **kwargs):
        ad = get_object_or_404(Ad, pk=kwargs['pk'])
        Click.objects.create(ad=ad, ip=self.ip)
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
        q1 = Ad.objects.values('id', 'name', 'views__time__year', 'views__time__month', 'views__time__day', 'views__time__hour').annotate(total_count=Count('clicks',distinct=True)+Count('views',distinct=True)).order_by()
        context['first_stats'] = q1
        return context


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

