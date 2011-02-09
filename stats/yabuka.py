import sys
import urllib, urllib2, cookielib
from BeautifulSoup import BeautifulSoup as B, BeautifulStoneSoup as X
from models import SiteStat, YabukaChannel, YabukaBids
from datetime import datetime
import time
import re
import string
import json

yabuka_username, yabuka_password = 'jacobgriffin', 'bigmoney2011'
campaign_category = 'diet'
campaign_name = 'diet2'
campaign_id = 807

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
yabuka_auth = urllib.urlencode({'username':yabuka_username,'password':yabuka_password})
yabuka_login_url = 'http://yabuka.com/account/login'
yabuka_browser = opener.open(yabuka_login_url, yabuka_auth)
    
    
def update_my_bid(channel_id, p2):
    yabuka_bid_post = 'http://yabuka.com/advertiser/campaign/807/ajax/set_bid'
    bid_info = urllib.urlencode({'channel_id':channel_id, 'amount':p2})
    yabuka_channel_top_bid = opener.open(yabuka_bid_post, bid_info).read()
    print yabuka_channel_top_bid
def get_channel_name_from_id(id):
    try:
        y = YabukaChannel.objects.get(channel_id = id)
        return y.channel_name 
    except YabukaChannel.DoesNotExist:
        return "unknown channel"
    
def get_top_bid(id, my_bid):
    yabuka_top_bid_url = 'http://yabuka.com/advertiser/campaign/'+str(campaign_id)+'/ajax/topbid_info'
    update_bid_values = urllib.urlencode({'channel_id':id})
    try:
        
        yabuka_channel_top_bid = opener.open(yabuka_top_bid_url, update_bid_values).read()        
        d = json.loads(yabuka_channel_top_bid)
        (p1,p2) = (d['positions']['1'], d['positions']['2'])

    except:
        p1 = my_bid
        p2 = my_bid
    if p2 is None: #I'm the top bid, perhaps we can lower it by 1 penny
        # or maybe we should lower by how much the top guy has lowere his bid.
        if p1 > 0 and p1 > my_bid:
            print 'calling top delta %s'%id 
            top_bid_delta = -0.01 #use this backup for now!
            #top_bid_delta = get_top_bid_delta(id, p1)
            if top_bid_delta is None:
                top_bid_delta = -0.01
        else:
            top_bid_delta = -0.01
        update_my_bid(id, my_bid + top_bid_delta)
        print '%s: %s lowered' % (get_channel_name_from_id(id), 
                                                        my_bid)
        p2 = my_bid + top_bid_delta
    elif p2 > my_bid or p2 < my_bid:    
        update_my_bid(id,p2)
        print '%s, %s -> %s' % (get_channel_name_from_id(id), 
                                                            p2, my_bid)
    else:
        print '%s: %s = %s'%(get_channel_name_from_id(id), p2,my_bid)
   
    #except urllib2.HTTPError:
    #    print 'error'
    #    p1,p2 = (0.00,0.00)
    return (p1,p2)

#def get_top_bid_delta(id, p1):
#    if p1 > YabukaBids.objects.all().filter(channel_id = id).order_by('-pk')[0].bid1:
#        return float(p1 - YabukaBids.objects.all().filter(channel_id = id).order_by('-pk')[0].bid1)
#    else:
#        return float(YabukaBids.objects.all().filter(channel_id = id).order_by('-pk')[0].bid1 - p1)


def get_channel_stats():
    yabuka_channel_url = 'http://yabuka.com/advertiser/campaign/'+str(campaign_id)
    yabuka_channels = opener.open(yabuka_channel_url).read()
    soup = B(yabuka_channels)
    xsoup = X(yabuka_channels)
    #return (soup, yabuka_channels)
    #Parse id and channel name from this
    #<td class=""><label for="flag-589" >Today.MSNBC.MSN.com</label></td>
    
    channel_list = []
    current_bid_list = []
    channel_id_list = []
    top_bids_list = []
    for o in xsoup.findAll(attrs={"for":re.compile('flag')}):
        channel_list.append(o.string)
    for o in soup.findAll("input", {"value":re.compile('\d\.\d\d')}):
        current_bid_list.append(float(o.attrs[5][1]))
        channel_id_list.append(int(string.replace(o.attrs[4][1],'setbid-','')))
        top_bids_list.append(get_top_bid(channel_id_list[-1],current_bid_list[-1]))
    #print channel_list
    #print current_bid_list
    #print channel_id_list
    #print top_bids_list
    #return (channel_list, current_bid_list, channel_id_list, top_bids_list)
    ensure_or_add_channels(zip(channel_list,channel_id_list))
    save_top_bids(campaign_name,campaign_id,campaign_category,
                  zip(channel_id_list, top_bids_list, current_bid_list))


def ensure_or_add_channels(channel_tuple):
    for c in channel_tuple:
        try:
            YabukaChannel.objects.get(channel_id = c[1])
        except YabukaChannel.DoesNotExist:
            y = YabukaChannel()
            (y.channel_name, y.channel_id) = (str(c[0]), c[1])
            y.save()
        
    
def save_top_bids(campaign_name, campaign_id, category, bid_list):
    for stat in bid_list:
        yb = YabukaBids()
        yb.stat_date = datetime.now()
        yb.channel_id = stat[0]
        yb.my_bid = stat[2]
        yb.bid1 = stat[1][0] #gets the 1st bid
        yb.bid2 = stat[1][1] #gets the 2nd bid
        yb.campaign_name = campaign_name
        yb.campaign_id = campaign_id
        yb.campaign_category = category
        yb.save()


def get_stats():    
    yabuka_browser = opener.open(yabuka_login_url, yabuka_auth)
    yabuka_stats_url = 'http://yabuka.com/advertiser/reports/'+str(campaign_id)
    date_range_today = urllib.urlencode({'date_start':'2011-03-05','date_end':'2011-03-05'})
    yabuka_stats = opener.open(yabuka_stats_url+'?%s', date_range_today).read()

    #Now to parse all that data. One yabuka row looks like this
    # <tr class="datarow">
    #        <td class="channels">Citadel Broadcasting Corp.</td>
    #        <td class="impressions">0</td>
    #        <td class="clicks">0</td>
    #        <td class="avg_cpc">$0.00</td>
    #       <td class="ctr">0.00%</td>
    #        <td class="avg_pos">0.00</td>
    #        <td class="cpa">$0.00</td>
    #        <td class="spend">$0.00</td>
    #        <td class="adv_reports">
    #          <a href="/advertiser/reports/807/geoloc?channel_id=611&date_end=2011-02-02&date_start=2011-02-02">Geo Report</a>
    #        </td>
    #      </tr>
    
    
    soup = B(yabuka_stats)
    regex = ",|\$|\%"
    stat_list = []
    for o in soup.findAll("tr", {"class":"datarow"}):
        site = SiteStat()
        site.ad_network = 'yabuka'
        site.site_name = str(o.contents[1].string)
        site.c_impressions = int(str(o.contents[3].string).replace(',',''))
        site.c_clicks = int(str(o.contents[5].string).replace(regex,''))
        site.c_cpc = float(str(o.contents[7].string).replace('$',''))
        site.c_ctr = float(str(o.contents[9].string).replace('%',''))
        site.avg_pos = float(str(o.contents[11].string))
        site.cpa = float(str(o.contents[13].string).replace('$','').replace(',',''))
        site.c_cost = float(str(o.contents[15].string).replace('$','').replace(',',''))
        site.c_sales = int(site.c_cost / site.cpa) if site.cpa > 0 else 0
        site.c_profit = 35*int(site.c_sales) - float(site.c_cost)
        site.c_profit_per_click = site.c_profit/site.c_clicks if site.c_clicks > 0 else 0
        site.c_revenue = 35*int(site.c_sales)

        try:
            previous_entry = SiteStat.objects.all().order_by('-pk')[0]
        except IndexError:
            previous_entry = 0
        if previous_entry:
            site.set = previous_entry.stat_set + 1 if previous_entry.stat_set == 0 else 1
            site.d_impressions = site.c_impressions - previous_entry.c_impressions
            site.d_clicks = site.c_clicks - previous_entry.c_clicks
            site.d_cpc = site.c_cpc - previous_entry.c_cpc
            site.d_sales = site.c_sales - previous_entry.c_sales
            site.d_cost = site.c_cost - previous_entry.c_cost
            site.d_revenue = site.c_revenue - previous_entry.c_revenue
            site.d_profit = site.c_profit - previous_entry.c_profit
            site.d_profit_per_click = site.c_profit_per_click - previous_entry.c_profit_per_click
            site.d_ctr = site.c_ctr - previous_entry.c_ctr
        stat_list.append(site)
        site.save()

def switch_to_ad_id(ad_id):
    print 'switching to: '+str(ad_id)
    for c in YabukaChannel.objects.all():
        ad_url = 'http://yabuka.com/advertiser/campaign/807/ajax/switch_ad/'+str(c.channel_id)
        new_ad_post = urllib.urlencode({'ad_id':ad_id})
        json_result = opener.open(ad_url, new_ad_post).read()  
        print json.loads(json_result)
        
        
def rotate_ads():
    current_ad_id = 1371
    while True:
        if current_ad_id == 1371:
            current_ad_id = 1389
        else:
            current_ad_id = 1371
        switch_to_ad_id(current_ad_id)
        print "finished at %s" %datetime.now()
        time.sleep(300)
def run_loop():
    i = 0
    while True:    
        i+=1
        print "Time now: %s" %datetime.now()
        get_stats()
        get_channel_stats()
        print "finished at %s" %datetime.now()
        time.sleep(300)
        
        
        
def set_my_bid(id, increment=0):
    pass
def get_top_bids(id):
    pass

