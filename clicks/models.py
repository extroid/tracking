from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime
class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name=_(u'Category')
        verbose_name_plural=_(u'Categories')
    
    def __unicode__ (self):
        return self.name

class CpaNetwork(models.Model):
    name = models.CharField(max_length=30, null = True) 
    login = models.CharField(max_length=30, null = True) 
    affiliate_id = models.CharField(max_length=30, null = True)
    password = models.CharField(max_length=30, null = True)
    
    class Meta:
        verbose_name=_(u'CpaNetwork')
        verbose_name_plural=_(u'CpaNetworks')
        
    def __unicode__ (self):
        return self.name
    
class LandingSite(models.Model):
    page1_template = models.CharField(max_length=30)
    page1_name = models.CharField(max_length=30)
    page1_desc = models.CharField(max_length=200, null = True)
    category = models.ForeignKey(Category, related_name='landing_sites')
    total_offers = models.IntegerField()
    exit_page_template  = models.CharField(max_length=30, null = True)
    redirect_on_exit = models.BooleanField(default = False)
    traffic_ratio = models.IntegerField(default = 100)
    active = models.BooleanField(default = False)
    
    class Meta:
        verbose_name=_(u'Landing site')
        verbose_name_plural=_(u'Landing sites')
    
    def __unicode__ (self):
        return '%s/%s offers %d ratio %d' % (self.category, self.page1_name, self.total_offers, self.traffic_ratio)

class Offer(models.Model):
    network = models.ForeignKey(CpaNetwork)
    name = models.CharField(max_length=30)
    url = models.URLField()
    offer_id = models.CharField(max_length=10, null = True)
    payout = models.FloatField()
    display_name = models.CharField(max_length=30, null=True)
    active = models.BooleanField(default=False)
    coupon = models.CharField(max_length=10, null=True)
    price_old = models.CharField(max_length=10, null=True)
    price_new = models.CharField(max_length=10, null=True)
    
    class Meta:
        verbose_name=_(u'Offer')
        verbose_name_plural=_(u'Offers')
        
    def __unicode__ (self):
        return '%s/%s payout %d' % (self.network.name, self.name, self.payout)
        
class DomainOfferSet(models.Model):
    name = models.CharField(max_length = 50)
    
    class Meta:
        verbose_name=_(u'Domain offer set')
        verbose_name_plural=_(u'Domain offer sets')
        
    def __unicode__ (self):
        return self.name
    
class OfferSet(models.Model):
    offer1 = models.ForeignKey(Offer, related_name = "first_offer")
    offer2 = models.ForeignKey(Offer, related_name = "second_offer", null = True)
    total_offers = models.IntegerField()
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='offer_sets')
    active = models.BooleanField(default=False)
    domain = models.ForeignKey(DomainOfferSet)

    class Meta:
        verbose_name=_(u'Offer set')
        verbose_name_plural=_(u'Offer sets')
        
    def __unicode__ (self):
        return '%s/%s/%s' % (self.domain, self.category, self.name)

class Visitor(models.Model):
    date_time = models.DateTimeField(default = datetime.datetime.now())
    referer = models.URLField(max_length=4096, null = True, blank=True)
    ip_address = models.IPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, null=True, blank=True)
    query_dict = models.CharField(max_length=300, null=True, blank=True)
#    click_id = models.CharField(max_length=100, null=True, blank=True)
    adsource = models.CharField(max_length=30, null=True, blank=True)
    account = models.CharField(max_length=30, null=True, blank=True)
    agegroup = models.CharField(max_length=30, null=True, blank=True)
    image = models.CharField(max_length=30, null=True, blank=True)
    channel = models.CharField(max_length=30, null=True, blank=True)
    testing = models.CharField(max_length=30, null=True, blank=True)
    safeview = models.CharField(max_length=30, null=True, blank=True )
    campaign = models.CharField(max_length=30,null=True, blank=True )
    domain = models.ForeignKey(DomainOfferSet, related_name='visitors')
    ad = models.CharField(max_length=30,null=True, blank=True)
    category = models.ForeignKey(Category, related_name='visitors')
    topic_name = models.CharField(max_length=50,null=True, blank=True)
    site = models.ForeignKey(LandingSite, related_name = "site",null=True, blank=True)
    offerset = models.ForeignKey(OfferSet, null = True,blank=True )
    offer1 = models.ForeignKey(Offer, related_name = "offer1",null=True)
    offer2 = models.ForeignKey(Offer, related_name = "offer2", null=True)
    offer1_click = models.BooleanField(default=False)
    offer2_click = models.BooleanField(default=False)
    offer1_sale = models.BooleanField(default=False)
    offer2_sale = models.BooleanField(default=False)
    offer1_link_tag = models.CharField(max_length=10, null=True)
    offer2_link_tag = models.CharField(max_length=10, null=True)
    offer_1_exit_sale = models.BooleanField(default=False)
    offer_2_exit_sale = models.BooleanField(default=False)
    cost_per_click = models.FloatField(blank=True, null=True,default=0)
    offer_1_revenue = models.FloatField(blank=True, null=True,default=0)
    offer_2_revenue = models.FloatField(blank=True, null=True,default=0)
    
    class Meta:
        verbose_name=_(u'Visitor')
        verbose_name_plural=_(u'Visitors')
        
    def __unicode__ (self):
        return '%s -> %s %s' % (self.referer, self.account, self.campaign)
        
class SiteOfferSet(models.Model):
    site = models.ForeignKey(LandingSite)
    offer_set = models.ForeignKey(OfferSet)
    traffic_ratio = models.IntegerField(default = 100)
    active = models.BooleanField(default = True)
    
    class Meta:
        verbose_name=_(u'Site offer set')
        verbose_name_plural=_(u'Site offer sets')
        
    def __unicode__ (self):
        return '%s/%s ratio %d' % (self.site, self.offer_set, self.traffic_ratio)
    