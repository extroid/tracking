# Create your views here.
from models import Visitor, LandingSite, OfferSet, Offer, SiteOfferSet, DomainOfferSet
from django.http import HttpResponse, HttpResponseRedirect
import random, urllib, datetime
from django.shortcuts import render_to_response, redirect


category_list = ['diet', 'finance', 'dating', 'penny-auction','skin-care']
force_domain_offerset = False

def show_main_page(request, category):
    #brand new visitor!
    v = create_visitor(request)
    v.category = category
    if not valid_category(v): #make sure the category is in the list
        return HttpResponse('Category %s is not valid'%category)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    v.save()
    name, link = get_template_fields(v)
    return render_to_response('%s/%s' % (v.category,v.site.page1_template), locals())

def go_to_offer(request, visitor_id, position, someid=None, linktag=None):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    aff_link = 0
    if position == '1':
        aff_link = Offer.objects.get(pk = v.offerset.offer1.id).offer_url
    elif position == '2':
        aff_link = Offer.objects.get(pk = v.offerset.offer2.id).offer_url
    redirect_url = str(aff_link)+str(create_subid(v,position))
    return redirect(redirect_url)

def show_exit_page(request, visitor_id):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    name, link = get_template_fields(v,exit=True)
    return render_to_response('%s/%s' % (v.category,v.site.exit_page_template), locals())




def go_to_offer_from_exit(request, visitor_id, position, someid=None, linktag=None):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    aff_link = 0
    if position == '1':
        aff_link = Offer.objects.get(pk = v.offerset.offer1.id).offer_url
    elif position == '2':
        aff_link = Offer.objects.get(pk = v.offerset.offer2.id).offer_url
    redirect_url = str(aff_link)+str(create_subid(v,position,exit=True))
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
        return LandingSite.objects.filter(category=v.category).order_by('?')[:1][0]#return 1st object in list
    else:
        return v.site
    
def get_visitor_offerset(v):
    if not v.offerset:
        if force_domain_offerset: #We match certain domains with certain offersets
            domain_offer_set = DomainOfferSet.objects.filter(domain_name = v.domain)[0]
            return OfferSet.objects.filter(category=v.category, domain = domain_offer_set).order_by('?')[:1][0]
        return OfferSet.objects.filter(category=v.category).order_by('?')[:1][0]
    else:
        return v.offerset

def get_template_fields(v,exit=False):
    if exit:
        exitstr = '/exitclick/'#clicks from exit page
    else:
        exitstr = '/redirect/'#clicks from main page
    name = [v.site, v.offerset.offer1.offer_name, v.offerset.offer2.offer_name ]
    link = [v.site, exitstr+str(v.id)+'/1',
                    exitstr+str(v.id)+'/2']
    #outgoing/visitor_id/offer_id/offer_position
    return (name, link)
    
def create_visitor(request):
    v = Visitor()
    #get params
    (v.referer, v.user_agent, v.domain) = (request.META.get('HTTP_REFERER'), 
                                         request.META.get('HTTP_USER_AGENT'),
                                         request.META.get('HTTP_HOST'),
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
    return v

def valid_category(v):
    if v.category not in category_list:
        return False
    else:
        return True
    
def create_subid(v,position,linktag=None,exit=False):
    if exit:
        exit = '-ex'
    return "v:"+str(v.id)+"-p:"+position+"-l:"+str(linktag)+str(exit)