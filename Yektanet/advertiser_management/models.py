from django.db import models
from PIL import Image 


class BaseAdvertising(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name 
    
    def __repr__(self) -> str:
        return self.name 
    
    class Meta:
        abstract = True

class Advertiser(BaseAdvertising):
    pass 

class Ad(BaseAdvertising):
    link = models.URLField(max_length=200)
    img = models.ImageField(upload_to ='images/')
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name="ads")
    approved = models.BooleanField(default=False)

    def save(self):      
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

    @property
    def image_url(self):

        if self.img:
            return getattr(self.img, 'url', None)
        return None


class Action(models.Model):

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
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



