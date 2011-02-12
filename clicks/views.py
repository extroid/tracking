# Create your views here.
from models import Visitor, LandingSite, OfferSet, Offer, SiteOfferSet, DomainOfferSet, Category, CpaNetwork
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import *
import random, urllib, datetime
from django.shortcuts import render_to_response, redirect
import logging
from django.core.exceptions import ValidationError
import sys

category_list = ['diet', 'finance', 'dating', 'penny-auction','skin-care']
force_domain_offerset = True

def show_main_page(request, category):
    #brand new visitor!
    try:
        v = create_visitor(request)
        v.category = get_object_or_404(Category, name=category)
        v.site = get_visitor_site(v)
        v.offerset = get_visitor_offerset(v)
        # v.full_clean()
        v.save()
        name, link, coupon, old_price, new_price, tomorrow, today = get_template_fields(v)
        return render_to_response('%s/%s' % (v.category.name,v.site.page1_template), locals())
    except (ValidationError, Http404), msg:
        logging.error(msg, exc_info=sys.exc_info(), extra={'url': request.build_absolute_uri()})    
        raise Http404

def go_to_offer(request, visitor_id, position, linktag=None):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    aff_link = 0
    if position == '1':
        aff_link = Offer.objects.get(pk = v.offerset.offer1.id).url
    elif position == '2':
        aff_link = Offer.objects.get(pk = v.offerset.offer2.id).url
    redirect_url = str(aff_link)+str(create_subid(v,position,linktag=linktag))
    return redirect(redirect_url)

def show_exit_page(request, visitor_id):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    name, link, coupon, old_price, new_price, tomorrow, today = get_template_fields(v,exit=True)
    return render_to_response('%s/%s' % (v.category.name,v.site.exit_page_template), locals())




def go_to_offer_from_exit(request, visitor_id, position, linktag=None):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    aff_link = 0
    if position == '1':
        aff_link = Offer.objects.get(pk = v.offerset.offer1.id).url
    elif position == '2':
        aff_link = Offer.objects.get(pk = v.offerset.offer2.id).url
    redirect_url = str(aff_link)+str(create_subid(v,position, linktag=linktag, exit=True))
    return redirect(redirect_url)





def get_offer_from_set():
    pass
#returns tuple of offers
#if position is given, returns 1 offer



#Helper functions
def get_visitor(visitor_id):
    return Visitor.objects.get(pk = visitor_id)
def get_visitor_site(v):
    if not v.site:
        return LandingSite.objects.filter(category=v.category).order_by('?')[0]#return 1st object in list
    else:
        return v.site
    
def get_visitor_offerset(v):
    if not v.offerset:
        if force_domain_offerset: #We match certain domains with certain offersets
            qset = OfferSet.objects.filter(category=v.category, domain = v.domain)
            if qset.count()>0:
                return OfferSet.objects.filter(category=v.category, domain = v.domain).order_by('?')[0]
            else:
                logging.error('There is no offer set for given visitor (%s, %s, %s)' % (v.referer, v.domain, v.adsource) )
                raise Http404
        return OfferSet.objects.filter(category=v.category).order_by('?')[0]
    else:
        return v.offerset

def get_template_fields(v,exit=False):
    if exit:
        exitstr = '/exitclick/'#clicks from exit page
    else:
        exitstr = '/redirect/'#clicks from main page
    name = [v.site, v.offerset.offer1.name, v.offerset.offer2.name ]
    link = [v.site, exitstr+str(v.id)+'/1',
                    exitstr+str(v.id)+'/2']
    coupon =  [v.site, v.offerset.offer1.coupon, v.offerset.offer2.coupon ]
    old_price =  [v.site, v.offerset.offer1.price_old, v.offerset.offer2.price_old ]
    new_price =  [v.site, v.offerset.offer1.price_new, v.offerset.offer2.price_new ]
    
    todayDate = datetime.date.today()
    tomorrowDate = todayDate + datetime.timedelta(days=1)
    today = todayDate.strftime('%A, %B %d, %Y')
    tomorrow = tomorrowDate.strftime('%A, %B %d, %Y')
    #outgoing/visitor_id/offer_id/offer_position
    return (name, link, coupon, old_price, new_price, tomorrow, today)
    
def create_visitor(request):
    v = Visitor()
    #get params
    try:
        v.referer = request.META.get('HTTP_REFERER')
    except KeyError, msg:
        logging.error(msg, exc_info=sys.exc_info(), extra={'url': request.build_absolute_uri()})
    try:        
        v.user_agent = request.META.get('HTTP_USER_AGENT')
    except KeyError, msg:
        logging.error(msg, exc_info=sys.exc_info(), extra={'url': request.build_absolute_uri()})
        
    try:    
        v.domain = get_object_or_404(DomainOfferSet, name=request.META.get('HTTP_HOST'))
    except KeyError, msg:
        logging.error(msg, exc_info=sys.exc_info(), extra={'url': request.build_absolute_uri()})    
    
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
     
    return v

def valid_category(v):
    if v.category not in category_list:
        return False
    else:
        return True
    
def create_subid(v,position,linktag=None,exit=False):
    if exit:
        exit = '-ex'
    return "v:"+str(v.id)+"-p:"+position+"-l:"+str(linktag)+"-ex:"+str(exit)