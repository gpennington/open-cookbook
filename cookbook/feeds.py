from django.contrib.syndication.views import Feed
from cookbook.models import *

class LatestRecipesFeed(Feed):
    title = "Latest Recipes from Open Cook Book"
    link = "/recipes/"
    description = "Grab the latest recipes and submissions to our recipe collection"

    def items(self):
        return Recipe.objects.order_by('-id')[:10]

    def item_title(self, item):
        return item.title
    
    def item_link(self, item):
        return item.get_absolute_url()


    def item_description(self, item):
        return item.directions
    