from django.contrib import admin
from .models import Advertiser, Ad 

@admin.register(Advertiser) 
class AdvertiserAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', )

@admin.register(Ad) 
class AdAdmin(admin.ModelAdmin):
    list_display = ('name', 'advertiser', 'link', 'approved')
    fields = ('name', 'link', 'img', 'advertiser', 'approved')
    list_filter = ('approved',)
    search_fields = ('name', )