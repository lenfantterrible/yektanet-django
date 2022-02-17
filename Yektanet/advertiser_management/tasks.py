from celery import shared_task
from .models import DailyStats, HourlyStats, Ad, Click, View
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count 

@shared_task(name='hourly_task')
def hourly_task():

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

@shared_task(name='daily_task')
def daily_task():

    ad_set = Ad.objects.all()
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)

    for ad in ad_set.iterator():
        clicks = Click.objects.filter(ad=ad, time__range = (today, tomorrow)).aggregate(count=Count('*'))
        views = View.objects.filter(ad=ad, time__range = (today, tomorrow)).aggregate(count=Count('*'))

        if(DailyStats.objects.filter(ad=ad).exists()):
            stats = DailyStats.objects.get(ad=ad)

        else:
            stats = DailyStats()
            stats.ad = ad 
        
        stats.clicks_count = clicks['count']
        stats.views_count = views['count']
        stats.save()     
        
    return f'Done!'