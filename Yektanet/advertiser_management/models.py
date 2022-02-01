from django.db import models

class BaseAdvertising(models.Model):

    name = models.CharField(max_length=50)
    clicks = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

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
    img = models.ImageField(upload_to ='uploads/% Y/% m/% d/')