from django.conf.urls.defaults import *
from cookbook.feeds import LatestRecipesFeed
from cookbook.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', homepage),
    url(r'^recipe/(?P<category_slug>[-\w]+)/(?P<recipe_slug>[-\w]+)/$', view_recipe, name="recipe_view"),
    url(r'^recipes/$', recipes, name="recipes_view"),
    url(r'^top-rated/$', top_rated, name="top_rated_view"),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', tag, name="tag_view"),
    url(r'^category/(?P<category_slug>[-\w]+)/$', category, name="category_view"),
    url(r'^search/$', search, name="search_view"),
    url(r'^feeds/recipe/$', LatestRecipesFeed()),
    url(r'^add/$', add, name="add_view"),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^api/', include('cookbook.api.urls')),

)


