# Create your views here.
from models import Visitor, LandingSite, OfferSet, Offer, SiteOfferSet, DomainOfferSet, Category, CpaNetwork
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import *
from django.template import RequestContext
import random, urllib, datetime
from django.shortcuts import render_to_response, redirect
import logging
from django.core.exceptions import ValidationError
import sys
import settings

from forms import SalesForm

category_list = ['diet', 'finance', 'dating', 'penny-auction','skin-care']
force_domain_offerset = True

def index(request):
    return render_to_response("index.html")
 
def show_main_page(request, category):
    #return HttpResponse(category)    
    #brand new visitor!
    try:
        v = create_visitor(request)
        v.category = get_object_or_404(Category, name=category)
        v.site = get_visitor_site(v)
        v.offerset = get_visitor_offerset(v)
        # v.full_clean()
        v.save()
        STATIC_URL = settings.MEDIA_URL
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
        v.offer1_click = True
    elif position == '2':
        aff_link = Offer.objects.get(pk = v.offerset.offer2.id).url
        v.offer2_click = True
    v.save()
        
    redirect_url = str(aff_link)+str(create_subid(v,position,linktag=linktag))
    #return redirect(redirect_url)
    return render_to_response('outbound.htm', locals())

def show_exit_page(request, visitor_id):
    v = get_visitor(visitor_id)
    v.site = get_visitor_site(v)
    v.offerset = get_visitor_offerset(v)
    name, link, coupon, old_price, new_price, tomorrow, today = get_template_fields(v,exit=True) 
    STATIC_URL = settings.MEDIA_URL                    
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
    #return redirect(redirect_url)
    return render_to_response('outbound.htm', locals())

def hide_referer_and_exit(url):
    #This function was put to hide the referer.
    #It uses a template called 'outbound.htm'
    #Which is send a simple url to meta refresh to
    return render_to_response('outbound.htm', url)

def get_offer_from_set():
    pass
#returns tuple of offers
#if position is given, returns 1 offer



#Helper functions
def get_visitor(visitor_id):
    return Visitor.objects.get(pk = visitor_id)
def get_visitor_site(v):
    if not v.site:
        return LandingSite.objects.filter(category=v.category, active=True).order_by('?')[0]#return 1st object in list
    else:
        return v.site
    
def get_visitor_offerset(v):
    if not v.offerset:
        if force_domain_offerset: #We match certain domains with certain offersets
            qset = OfferSet.objects.filter(category=v.category, domain = v.domain, active=True)
            if qset.count()>0:
                return OfferSet.objects.filter(category=v.category, domain = v.domain, active=True).order_by('?')[0]
            else:
                logging.error('There is no offer set for given visitor (%s, %s, %s)' % (v.referer, v.domain, v.adsource) )
                raise Http404
        return OfferSet.objects.filter(category=v.category, active=True).order_by('?')[0]
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
     v.safeview, v.topic_name) = (request.GET.get('adsource','missing'),
                                      request.GET.get('account','missing'),
                                      request.GET.get('ad','missing'),
                                      request.GET.get('agegroup','missing'),
                                      request.GET.get('image','missing'),
                                      request.GET.get('channel','missing'),
                                      request.GET.get('testing','missing'),
                                      request.GET.get('safeview','missing'),
                                      request.GET.get('topicname','missing'),
                                      )
     
    return v

def valid_category(v):
    if v.category not in category_list:
        return False
    else:
        return True

def register_sales(request):
    if request.method=='GET':
        salesForm = SalesForm()
        return render_to_response("reg_sales_form.html", 
                                  {'form': salesForm},
                                  context_instance=RequestContext(request))
    elif request.method=='POST':
        salesForm = SalesForm()
        if request.POST:
            
            subids = request.POST['subids'].split('\n')
            message = None
            for subid in subids:
                try:
                    values = subid.split('-')
                    vid = vpos = linktag = exit_val = None
                    if len(values)==5:
                        exit_val = '-ex'
                    else:
                        exit_val = values[3].split(':')[1].strip(' ') # offer_1_exit_sale    
                    vid = int(values[0].split(':')[1])    
                    vpos = values[1].split(':')[1].strip(' ') # offer_1_sale
                    linktag = values[2].split(':')[1].strip(' ')
                except (IndexError, TypeError), msg:
                    logging.error(subid +' '+msg)
                    logging.error(msg)
                    message = 'During data process there were errors encountered. See error log for details'    
                try:
                    v = Visitor.objects.get(pk = vid)
                    if vpos=='1':
                        v.offer_1_sale = True if linktag!='None' else False
                        v.offer_1_linktag = linktag if linktag!='None' else None
                        v.offer_1_exit_sale = True if exit_val=='-ex' else False
                        v.offer_1_revenue = v.offerset.offer1.payout
                    elif vpos =='2':
                        v.offer_2_sale = True if linktag else False
                        v.offer_2_linktag = linktag if linktag!='None' else None
                        v.offer_2_exit_sale = True if exit_val=='-ex' else False
                        v.offer_2_revenue = v.offerset.offer2.payout
                    else:
                        logging.error(subid +' wrong position value '+vpos)
                        message = 'During data process there were errors encountered. See error log for details'
                    v.save()            
                except Visitor.DoesNotExist, msg:
                    logging.error(subid +' '+msg)    
                    message = 'During data process there were errors encountered. See error log for details'
                
            salesForm = SalesForm(initial={'subids':request.POST['subids']})    
            return render_to_response("reg_sales_form.html", 
                                      {'form': salesForm, 'message':message },
                                      context_instance=RequestContext(request))    
        else:
            return render_to_response("reg_sales_form.html", 
                                      {'form': salesForm, 'message': 'No data to process. Format v:1360-p:2-l:None-ex:False'},
                                      context_instance=RequestContext(request))    
    
def create_subid(v,position,linktag=None,exit=False):
    if exit:
        exit = '-ex'
    return "v:"+str(v.id)+"-p:"+position+"-l:"+str(linktag)+"-ex:"+str(exit)