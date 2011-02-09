from django.db import models
import datetime
from django.contrib import admin

# Create your models here.
class LandingSite(models.Model):
    page1_template = models.CharField(max_length=30)
    page1_name = models.CharField(max_length=30)
    page1_desc = models.CharField(max_length=200, null = True)
    category = models.CharField(max_length=30)
    total_offers = models.IntegerField()
    exit_page_template  = models.CharField(max_length=30, null = True)
    redirect_on_exit = models.BooleanField(default = False)
    traffic_ratio = models.IntegerField(default = 100)
    active = models.BooleanField(default = False)

class Offer(models.Model):
    network_name = models.CharField(max_length=30, null = True)
    offer_name = models.CharField(max_length=30)
    offer_url = models.URLField()
    offer_id = models.CharField(max_length=10, null = True)
    payout = models.FloatField()
    display_name = models.CharField(max_length=30, null=True)
    active = models.BooleanField(default=False)
    coupon = models.CharField(max_length=10, null=True)
    price_old = models.CharField(max_length=10, null=True)
    price_new = models.CharField(max_length=10, null=True)
    
        
class DomainOfferSet(models.Model):
    domain_name = models.CharField(max_length = 50)
    
class OfferSet(models.Model):
    offer1 = models.ForeignKey(Offer, related_name = "first_offer")
    offer2 = models.ForeignKey(Offer, related_name = "second_offer", null = True)
    total_offers = models.IntegerField()
    offerset_name = models.CharField(max_length=50)
    offerset_desc = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    domain = models.ForeignKey(DomainOfferSet)

class SiteOfferSet(models.Model):
    site = models.ForeignKey(LandingSite)
    offer_set = models.ForeignKey(OfferSet)
    traffic_ratio = models.IntegerField(default = 100)
    active = models.BooleanField(default = True)
    

class Visitor(models.Model):
    date_time = models.DateTimeField(default = datetime.datetime.now())
    referer = models.URLField(null = True)
    ip_address = models.IPAddressField(null=True)
    user_agent = models.CharField(max_length=100, null=True)
    query_dict = models.CharField(max_length=300, null=True)
    click_id = models.CharField(max_length=100, null=True)
    adsource = models.CharField(max_length=30, null=True)
    account = models.CharField(max_length=30, null=True)
    agegroup = models.CharField(max_length=30, null=True)
    image = models.CharField(max_length=30, null=True)
    channel = models.CharField(max_length=30, null=True)
    testing = models.CharField(max_length=30, null=True)
    safeview = models.CharField(max_length=30, null=True)
    campaign = models.CharField(max_length=30,null=True)
    domain = models.CharField(max_length=50,null=True)
    ad = models.CharField(max_length=30,null=True)
    category = models.CharField(max_length=30,null=True)
    topic_name = models.CharField(max_length=50,null=True)
    site = models.ForeignKey(LandingSite, related_name = "site",null=True)
    offerset = models.ForeignKey(OfferSet, null = True)
    offer1 = models.ForeignKey(Offer, related_name = "offer1",null=True)
    offer2 = models.ForeignKey(Offer, related_name = "offer2", null=True)
    offer1_click = models.BooleanField(default=False)
    offer2_click = models.BooleanField(default=False)
    offer1_sale = models.BooleanField(default=False)
    offer2_sale = models.BooleanField(default=False)
    offer1_link_tag = models.CharField(max_length=10, null=True)
    offer2_link_tag = models.CharField(max_length=10, null=True)
    cost_per_click = models.FloatField(null=True,default=1.00)
