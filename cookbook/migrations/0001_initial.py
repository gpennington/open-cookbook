# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Recipe'
        db.create_table('cookbook_recipe', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('directions', self.gf('django.db.models.fields.TextField')()),
            ('ingredients', self.gf('django.db.models.fields.TextField')()),
            ('tips', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('healthier_substitutions', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('image', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('image_upload', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('rating', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_to_twitter', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cookbook', ['Recipe'])


    def backwards(self, orm):
        
        # Deleting model 'Recipe'
        db.delete_table('cookbook_recipe')


    models = {
        'cookbook.recipe': {
            'Meta': {'ordering': "['-id']", 'object_name': 'Recipe'},
            'directions': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'healthier_substitutions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'image_upload': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {}),
            'publish_to_twitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'tips': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['cookbook']
