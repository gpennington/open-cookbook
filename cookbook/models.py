from django.db import models
from django.template.defaultfilters import slugify
from cookbook.choices import *
from tagging.fields import TagField
from tagging.models import Tag
import twitter
from settings.common import *
import bitly_api
from django.contrib.auth.models import User
from nutsbolts.utils.slugs import *

class RecipeManager(models.Manager):
    def published(self):
        return Recipe.objects.filter(published=True)
        
    def featured(self):
        return Recipe.objects.filter(published=True, featured=True)

class CategoryManager(models.Manager):
    def published(self):
        return Category.objects.filter(published=True)

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(editable=False)
    published = models.BooleanField()
    
    objects = CategoryManager()
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        unique_slugify(self, self.name)
        super(Category, self).save()
    
    @models.permalink
    def get_absolute_url(self):
        return ('cookbook.views.category', (), {'category_slug': self.slug})


class Recipe(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(editable=False)
    date_published = models.DateField(auto_now=True, auto_now_add=True)
    servings = models.CharField(max_length=10)
    total_cooking_time = models.CharField(max_length=30)
    source = models.CharField(max_length=250, blank=True, help_text='Please include page number')
    directions = models.TextField()
    ingredients = models.TextField()
    tips = models.TextField(blank=True)
    healthier_substitutions = models.TextField(blank=True)
    tags = TagField(help_text='Please use comma seperated values.')
    category = models.ForeignKey(Category)
    image = models.URLField(help_text='Please use flickr to host the image.', blank=True, editable=False)
    image_upload = models.ImageField(upload_to='cookbook/images/', blank=True)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    featured = models.BooleanField()
    published = models.BooleanField()
    publish_to_twitter = models.BooleanField()
    author = models.ForeignKey(User, null=True, blank=True, editable=False)
    
    objects = RecipeManager()

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.title

    def save(self):
        unique_slugify(self, self.title)
        if self.publish_to_twitter == True:
            
            twitter_api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY, consumer_secret=TWITTER_CONSUMER_SECRET, access_token_key=TWITTER_ACCESS_TOKEN, access_token_secret=TWITTER_ACCESS_SECRET)
            bitly = bitly_api.Connection(BITLY_USERNAME,BITLY_API_KEY)
        
            build_url = "http://cookbook.derekandlindy.com/recipe/" + self.slug
        
            short_url = bitly.shorten(build_url)
            twitter_api.PostUpdate("Just Cooked! " + self.title + " " + short_url['url'])
        super(Recipe, self).save()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    @models.permalink
    def get_absolute_url(self):
        return ('cookbook.views.view_recipe', (), {'category_slug': self.category.slug, 'recipe_slug': self.slug})
    
class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    bio = models.TextField(blank=True)
    twitter_username = models.CharField(max_length=140)
    image = models.ImageField(upload_to="iroam/images/proifiles", blank=True, null=True)
    
    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
        
    @models.permalink
    def get_absolute_url(self):
        return "/profile"

    
