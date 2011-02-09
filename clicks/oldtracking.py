

# Create your views here.
from models import Visitor, LandingSite, OfferSet, Offer, SiteOfferSet
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
import datetime
import random
from django.shortcuts import render_to_response, redirect
import urllib
#Traffic from adsonar, adblade, etc, end up here.
#This function decides, based on url params like: adnetwork, account, campaign, ad, date/time, siteList, OfferList, other rules
#Which site template should be loaded with params and displayed to the user
#Date is stored in the DB and a subid is used on all tracking links
#This tracking link is combined with the pageID and linkPositionID and timeStamp to display even better stats

#Every click to the page has to have one of these categories
category_list = ['diet', 'finance', 'dating', 'penny-auction','skin-care']
force_domain_offerset = True #Certain domains can only see certain offer sets

def incoming_click(request,category):
    '''Every page load creates a new visitor object.
    This visitor object is updated with a random site and offerset (combination of 2 offers), 
    then redirected to the page template.'''
    #To do: Use publisher component to send messages to any consumer... SendMessage(visitor)
    v = Visitor()
    #get params
    (v.referer, v.user_agent, v.domain, v.category) = (request.META.get('HTTP_REFERER'), 
                                         request.META.get('HTTP_USER_AGENT'),
                                         request.META.get('SERVER_NAME'),
                                         category,
                                         )
    #get url params
    (v.adsource, v.account, v.ad, v.agegroup,v.image, v.channel, v.testing, 
     v.safeview) = (request.GET.get('adsource','missing'),
                                      request.GET.get('account','missing'),
                                      request.GET.get('ad','missing'),
                                      request.GET.get('agegroup','missing'),
                                      request.GET.get('image','missing'),
                                      request.GET.get('channel','missing'),
                                      request.GET.get('testing','missing'),
                                      request.GET.get('safeview','missing'),
                                      )
    if category not in category_list:
        v.category = 'Error'
        v.save()
        return HttpResponse("Category %s was not found" % category)
    
    site = get_site(category)
    v.site = site
    v.offerset_id, offer_list = get_offerset(site)

    v.save()
    name,link = _get_display_name_and_link(v,offer_list)
    return render_to_response('%s/%s' % (v.category,site.page1_template), locals())


def _get_display_name_and_link(v,offer_list, exit=False):
    '''This function returns a tuple of offer names and outgoing links
    The exit param can be marked True to create an exit outgoing link'''
    if exit:
        exit = 'exit/'
    else:
        exit = ''
    name = [v.site] + [o.offer_name for o in offer_list] #In the template, we can call name.0 and name.1 for the offer names
    link = [v.site] + ['/outgoing/'+str(exit)+str(v.id)+'/'+str(o.id)+'/'+str(i+1)  for i,o in enumerate(offer_list)] #We call links the same way
    #The str(i + 1) uses the index from enumerate which starts at 0,1,2.. to keep track of offer positions
    #for the links. We want to start at 1, so we add 1 to i.
    #outgoing/visitor_id/offer_id/offer_position
    return (name,link)

def get_site(category):
    '''Get a random site object'''
    site = LandingSite.objects.filter(category=category).order_by('?')[:1]
    return site[0] #return random site

def get_offerset(site, v = False):
    '''Get the right number of offers and add it to a dictionary
    The offerset is basically created by looking up all the SiteOfferSet ids 
    where the site has a valid row for. This id list is then used to grab an offerset randomly'''
    #1. get list of offerset ids from siteofferset for this site
    #2. get offerSets from query filter by ids in list from previous step
    if v:
        offerset = OfferSet.objects.filter(pk = v.offerset_id)[:1]
    else:
        offerset = OfferSet.objects.filter(pk__in = 
                                       [sof.offer_set_id for sof in SiteOfferSet.objects.filter(site = site)]).order_by('?')[:1]
    offerset_list = []    
    if site.total_offers >= 1:
        o1 = Offer.objects.get(id=offerset[0].offer1_id)
        offerset_list.append(o1)
    if site.total_offers >= 2:
        o2 = Offer.objects.get(id=offerset[0].offer2_id)
        offerset_list.append(o2)
    return (offerset[0].id,offerset_list) # Return both the offerset.id and list. ID is returned so that visitor can be updated

def outgoing_click(request, tracking_id, offer_id,position_id,linktag="none"):
    return HttpResponse(offer_id)
    _user_clicked_offer(tracking_id, offer_id,position_id)
    return _redirect_to_offer(tracking_id, offer_id,position_id,linktag)

def outgoing_click_exit(request, tracking_id, offer_id,position_id,linktag="none"):
    _user_clicked_offer(tracking_id, offer_id,position_id)
    return _redirect_to_offer(tracking_id, offer_id,position_id,linktag,exit=True)


def _user_clicked_offer(tracking_id, offer_id,position_id):
    '''Update the visitor object with the offer number that was clicked'''
    v = Visitor.objects.get(pk=tracking_id)
    if position_id == 1:
        v.offer1_click = True
    elif position_id == 2:
        v.offer2_click = True
    v.save()

def _create_subid(tracking_id, offer_id,position_id,linktag,exit):
    if exit: #was this from the exit page, if so mark it as such
        exit = '-ex'
    else:
        exit = ''
    return "v:"+str(tracking_id)+"-o:"+offer_id+"-l:"+str(linktag)+str(exit)

def _redirect_to_offer(tracking_id, offer_id,position_id,linktag,exit):
    '''Append the visitor id and the linktag, if any, to the end of the url and send it on it's way'''
    subid = _create_subid(tracking_id, offer_id,position_id,linktag,exit)
    url = Offer.objects.get(pk=offer_id).offer_url+str(subid)
    #Send message(Visitor, OfferClicked)
    return redirect(url)


def trigger_exit_page(category,exit,visitor_id):
    v = Visitor.objects.get(pk = visitor_id)
    offer_list = get_offerset(v.site, v)
    name, link = _get_display_name_and_link(v, offer_list, True)
    return render_to_response('%s/%s' % (v.category,v.site.exit_page_template), locals())

    




#FOR TESTING ONLY!!!    
def create_dummy_objects():
    s = LandingSite()
    s.page1_template = 'acai1.html'
    s.page1_name = 'acai version 1'
    s.page1_desc = "Ben's site"
    s.category = 'diet'
    s.total_offers = 2
    s.active = True
    s.redirect_on_exit = True
    s.save()
    
    o = Offer()
    o.network_name = 'eadv'
    o.offer_name = 'Lean Spa US'
    o.offer_url = 'http://www.leanspa.com?s='
    o.display_name = 'Lean Spa'
    o.offer_id = 10107
    o.active = True
    o.payout = 50.00
    o.save()
    
    o2 = Offer()
    o2.network_name = 'eadv'
    o2.offer_name = 'ColoThin'
    o2.offer_url = 'http://www.colothin.com?s='
    o2.display_name = 'ColoThin'
    o2.offer_id = 2345
    o2.active = True
    o2.price_old = '3.99'
    o2.price_new = '1.99'
    o2.coupon = 'COLOSAVE'
    o2.payout = 50.00
    o2.save()
    
    os = OfferSet()
    os.offer1_id = 1
    os.offer2_id = 2
    os.total_offers = 2
    os.category = 'diet'
    os.active = True
    os.save()
    
    sof = SiteOfferSet()
    sof.site = s
    sof.offer_set = os
    sof.save()
    
    