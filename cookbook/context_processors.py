from cookbook.models import *
from django.contrib.comments.models import Comment
import twitter


def common_recipes(request):
    context = {}
    context['related_posts'] = Recipe.objects.published()[:3]
    context['popular_posts'] = Recipe.objects.published()[:3]
    context['photo_stream'] = Recipe.objects.published()[:6]
    context['global_comments'] = Comment.objects.all()[:3]
    context['category_list'] = Category.objects.published()
    twitter_api = twitter.Api()
    context['twitter_status'] = twitter_api.GetUserTimeline('opencookbook')
    return context