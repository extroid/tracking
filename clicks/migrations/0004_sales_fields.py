# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Visitor.offer_1_revenue'
        db.add_column('clicks_visitor', 'offer_1_revenue', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Visitor.offer_1_revenue'
        db.delete_column('clicks_visitor', 'offer_1_revenue')


    models = {
        'clicks.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'clicks.cpanetwork': {
            'Meta': {'object_name': 'CpaNetwork'},
            'affiliate_id': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        'clicks.domainofferset': {
            'Meta': {'object_name': 'DomainOfferSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'clicks.landingsite': {
            'Meta': {'object_name': 'LandingSite'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'landing_sites'", 'to': "orm['clicks.Category']"}),
            'exit_page_template': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page1_desc': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'page1_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pageTruemplate': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'redirect_on_exit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_offers': ('django.db.models.fields.IntegerField', [], {}),
            'traffic_ratio': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        'clicks.offer': {
            'Meta': {'object_name': 'Offer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'coupon': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clicks.CpaNetwork']"}),
            'offer_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'payout': ('django.db.models.fields.FloatField', [], {}),
            'price_new': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'price_old': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'clicks.offerset': {
            'Meta': {'object_name': 'OfferSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offer_sets'", 'to': "orm['clicks.Category']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clicks.DomainOfferSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'offer1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_offer'", 'to': "orm['clicks.Offer']"}),
            'offer2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'second_offer'", 'null': 'True', 'to': "orm['clicks.Offer']"}),
            'total_offers': ('django.db.models.fields.IntegerField', [], {})
        },
        'clicks.siteofferset': {
            'Meta': {'object_name': 'SiteOfferSet'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clicks.OfferSet']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clicks.LandingSite']"}),
            'traffic_ratio': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        },
        'clicks.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'ad': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'adsource': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'agegroup': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitors'", 'to': "orm['clicks.Category']"}),
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'cost_per_click': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 2, 14, 12, 2, 48, 390166)'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitors'", 'to': "orm['clicks.DomainOfferSet']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'offer1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offer1'", 'null': 'True', 'to': "orm['clicks.Offer']"}),
            'offer1_click': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offer1_link_tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'offer1_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offer2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offer2'", 'null': 'True', 'to': "orm['clicks.Offer']"}),
            'offer2_click': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offer2_link_tag': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'offer2_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offer_1_exit_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offer_1_revenue': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'offer_2_exit_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'offer_2_revenue': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'offerset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['clicks.OfferSet']", 'null': 'True', 'blank': 'True'}),
            'query_dict': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'referer': ('django.db.models.fields.URLField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'safeview': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'site'", 'null': 'True', 'to': "orm['clicks.LandingSite']"}),
            'testing': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'topic_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['clicks']
