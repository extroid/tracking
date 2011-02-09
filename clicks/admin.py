from django.contrib import admin
from models import LandingSite, Offer, OfferSet, SiteOfferSet, DomainOfferSet


admin.site.register(LandingSite)
admin.site.register(Offer)
admin.site.register(OfferSet)
admin.site.register(SiteOfferSet)
admin.site.register(DomainOfferSet)
