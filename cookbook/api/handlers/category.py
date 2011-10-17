from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import *
from cookbook.models import Category
from django.http import *
from django.shortcuts import *
from django.db.models import Q
from api_manager.utils import *
from sentry.client.models import client
import logging


   
class CategoryHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE', 'POST')
    model = Category
    fields = ('name', 'slug', 'id')
    
    def read(self, request, category_id=None):
        # if requesting all categories
        message_id = client.create_from_text('Read on Cookbook API Category', level=logging.INFO, url=None)
        if category_id == None:
            limit = request.GET.get('limit', 'all')
            if limit != 'all':
                base = Category.objects.published()[:limit]
            else:
                base = Category.objects.published()
            return base
        else:
            try:
                category = get_object_or_404(Category, pk=category_id)
            except Category.DoesNotExist:
                return rc.NOT_FOUND
            return category
        
    def create(self, request):
        if request.POST:
            attrs = self.flatten_dict(request.POST)
            category = Category(name=attrs['name'])
            category.published = True
            category.save()
            return category

    @throttle(10, 5)
    def delete(self, request, category_id):
        key_dict = {'key': request.GET.get('key')}
        if key_exists(key_dict) == False:
            return key_required_error()
        if key_check(key_dict):
            try:
                category  = Category.objects.get(pk=category_id)
                
            except Category.DoesNotExist:
                return rc.NOT_FOUND
            category.delete()
            #log_use(request.GET.get('key'), 'Recipe Category', category_id, 'deleted')
            return rc.DELETED
        else:
            return key_incorrect_error()
                        
    @throttle(10, 5)
    def update(self, request, category_id):
        attrs = self.flatten_dict(request.PUT)
        
        key_dict = {'key': request.GET.get('key')}
        
        if key_exists(key_dict) == False:
            return key_required_error()
        if key_check(key_dict):
            try:
                category = Category.objects.get(pk=category_id)
                
            except Category.DoesNotExist:
                return rc.NOT_FOUND
            
            category.name = attrs['name']
            category.save()
            return category
        else:
            return key_incorrect_error()
