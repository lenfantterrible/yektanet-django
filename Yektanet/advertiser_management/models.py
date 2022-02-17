from django.db import models
from PIL import Image 
from django.db.models import Count
import datetime
from django.contrib.auth.models import User

class BaseAdvertising(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name 
    
    def __repr__(self) -> str:
        return self.name 
    
    class Meta:
        abstract = True

class Advertiser(BaseAdvertising):
    
    author = models.ForeignKey(User, verbose_name=("author"), on_delete=models.CASCADE)
    @property
    def approved_ads(self):

        return self.ads.filter(approved=True)

class Action(models.Model):

    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True) 
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False)

    class Meta: 
        abstract = True 

class Click(Action): 
    
    class Meta:
        default_related_name = 'clicks'

class View(Action): 
    
    class Meta:
        default_related_name = 'views'

class Ad(BaseAdvertising):
    link = models.URLField(max_length=200)
    img = models.ImageField(upload_to ='images/')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name="ads")
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):      
        if not self.img:
            return 
        
        if self._state.adding:
            super(Ad, self).save()
            image = Image.open(self.img)
            (width, height) = image.size     
            size = ( 300, 300)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.img.path.replace(" ", "_"))
        else:
            super(Ad, self).save()

    def inc_views(self, ip):
        View.objects.create(ad=self, ip=ip)

    def inc_clicks(self, ip):
        Click.objects.create(ad=self, ip=ip)


    
    @property
    def stats(self): 

        out = dict()
        q1 = Click.objects.filter(ad=self).values('time__date', 'time__hour').annotate(count=Count('*')).order_by('-time__date', '-time__hour')
        q2 = View.objects.filter(ad=self).values('time__date', 'time__hour').annotate(count=Count('*')).order_by('-time__date', '-time__hour')

        for entry in q1:
            out[(entry['time__date'], entry['time__hour'])] = (0, entry['count'], 0, 0) 

        for entry in q2:
            key = (entry['time__date'], entry['time__hour'])
            if key in out:
                out[key] = (entry['count'], out[key][1], entry['count'] + out[key][1], out[key][1] * 100 / entry['count']) 
            else:
                out[key] = (entry['count'],0, entry['count'], 0) 

        return out

    @property
    def image_url(self):

        if self.img:
            return getattr(self.img, 'url', None)
        return None


class BaseStats(models.Model):

    ad = models.OneToOneField('Ad', on_delete=models.CASCADE, related_name='hourly_stats')
    clicks_count = models.PositiveIntegerField(verbose_name="Clicks Count")
    views_count = models.PositiveIntegerField(verbose_name="Clicks Count")

    def __str__(self) -> str:
        return f'({self.ad},{self.views_count},{self.clicks_count}' 
    
    def __repr__(self) -> str:
        return f'({self.ad},{self.views_count},{self.clicks_count}' 
    
    class Meta:
        abstract = True

class HourlyStats(BaseStats):
    pass

class DailyStats(BaseStats):
    pass