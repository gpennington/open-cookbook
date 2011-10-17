from django.conf.urls.defaults import *
from piston.resource import Resource
from cookbook.api.handlers.recipe import RecipeHandler, SingleRecipeHandler
from cookbook.api.handlers.category import CategoryHandler
from api_manager.utils import CsrfExemptResource


recipe_handler = CsrfExemptResource(RecipeHandler)
category_handler = CsrfExemptResource(CategoryHandler)
single_recipe_handler = CsrfExemptResource(SingleRecipeHandler)


urlpatterns = patterns('',
    url(r'^recipe$', recipe_handler),
    url(r'^recipe/(?P<recipe_id>\d+)$', single_recipe_handler),
    url(r'^category$', category_handler),
    url(r'^category/(?P<category_id>\d+)$', category_handler),
    

)