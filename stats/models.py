from django.db import models
#from django.contrib import admin
# Create your models here.

import datetime

class SiteStat(models.Model):
    '''A referer's total stat object for the day.
    Any site on a transparent ad network along with its
    total clicks, impressions, sales, etc for today.
    c_ means cumulative, d_ means differential, i.e., difference of last 2 rows'''
    ad_network = models.CharField(max_length=30, null = True)
    site_name = models.CharField(max_length=30, null = True)
    topic_name = models.CharField(max_length=30, null = True)
    pub_id = models.CharField(max_length=30, null = True)
    c_impressions = models.IntegerField(default = 0)
    c_clicks = models.IntegerField(default = 0)
    c_cpc = models.FloatField(default = 0)
    c_sales = models.IntegerField(default = 0)
    c_cost = models.FloatField(default = 0)
    c_revenue = models.FloatField(default = 0)
    c_profit = models.FloatField(default = 0)
    c_profit_per_click = models.FloatField(default = 0)
    c_ctr = models.FloatField(default = 0)
    d_impressions = models.IntegerField(default = 0)
    d_clicks = models.IntegerField(default = 0)
    d_cpc = models.FloatField(default = 0)
    d_sales = models.IntegerField(default = 0)
    d_cost = models.FloatField(default = 0)
    d_revenue = models.FloatField(default = 0)
    d_profit = models.FloatField(default = 0)
    d_profit_per_click = models.FloatField(default = 0)
    d_ctr = models.FloatField(default = 0)
    stat_set = models.IntegerField(default = 0)
    stat_date = models.DateTimeField(default = datetime.datetime.now())

class YabukaChannel(models.Model):
    channel_name = models.CharField(max_length = 50)
    channel_id = models.IntegerField()

class YabukaBids(models.Model):
    channel_id = models.IntegerField()
    stat_date = models.DateTimeField(default = datetime.datetime.now())
    bid1 = models.FloatField()
    bid2 = models.FloatField()
    my_bid = models.FloatField()
    strategy_suggested = models.CharField(null = True, max_length = 50, default = "none")
    strategy_employed = models.CharField(null = True, max_length = 50, default = "none")
    campaign_name = models.CharField(null = True, max_length = 50, default = "none")
    campaign_id = models.IntegerField()
    campaign_category = models.CharField(null = True, max_length = 50, default = "none")
    
    