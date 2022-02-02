from django.contrib import admin
from .models import Advertiser, Ad 

@admin.register(Advertiser) 
class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('name', 'clicks', 'views')
    fields = ('name', )

@admin.register(Ad) 
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'advertiser', 'link', 'clicks', 'views')
    fields = ('name', 'link', 'img', 'advertiser')