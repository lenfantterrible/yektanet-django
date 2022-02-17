from celery import shared_task
from .models import HourlyStats, Ad, Click, View
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count 

@shared_task(name='celery_task')
def celery_task():

    ad_set = Ad.objects.all()
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    one_hour_later = this_hour + timedelta(hours=1)

    for ad in ad_set.iterator():
        clicks = Click.objects.filter(ad=ad, time__range = (this_hour, one_hour_later)).aggregate(count=Count('*'))
        views = View.objects.filter(ad=ad, time__range = (this_hour, one_hour_later)).aggregate(count=Count('*'))

        if(HourlyStats.objects.filter(ad=ad).exists()):
            stats = HourlyStats.objects.get(ad=ad)

        else:
            stats = HourlyStats()
            stats.ad = ad 
        
        stats.clicks_count = clicks['count']
        stats.views_count = views['count']
        stats.save()     
        
    return f'Done!'