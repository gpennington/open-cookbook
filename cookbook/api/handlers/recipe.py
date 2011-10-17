from piston.handler import BaseHandler, AnonymousBaseHandler
from piston.utils import *
from cookbook.models import Recipe
from django.http import *
from django.shortcuts import *
from django.db.models import Q
from api_manager.utils import *

class RecipeHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Recipe
    fields = ('title', 'slug', 'source', 'directions', 'ingredients', 'tips', 'healthier_substitutions', 'tags', ('category', ('name', 'slug'),), 'image_upload', 'rating', 'featured', 'published')

    
    @throttle(10, 5)
    def read(self, request):
        limit = request.GET.get('limit', 'all')
        if limit != 'all':
            base = Recipe.objects.published()[:limit]
        else:
            base = Recipe.objects.published()
        return base
    

class SingleRecipeHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Recipe
    fields = ('title', 'slug', 'source', 'directions', 'ingredients', 'tips', 'healthier_substitutions', 'tags', ('category', ('name', 'slug'),), 'image_upload', 'rating', 'featured', 'published')
    
    @throttle(10, 5)
    def read(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return recipe