from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.simple import direct_to_template
from cookbook.models import *
from tagging.models import Tag, TaggedItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from cookbook.forms import *

'''
 - HOme page
 - Recipes by order of newest
  - Recipes that are most highly rated
 - search results
 - pagination for all max 8


'''
def get_related(title):
    search_query = title
    recipes = Recipe.objects.filter(Q(title__icontains=search_query) | Q(directions__icontains=search_query) | Q(ingredients__icontains=search_query))[:3]
    return recipes

def homepage(request):
    extra_context = {}
    recipes = Recipe.objects.published()
    extra_context['photo_recipes'] = Recipe.objects.published()[:12]
    extra_context['featured_recipes'] = Recipe.objects.featured()
    extra_context['slider_photos'] = Recipe.objects.featured()[:4]
    
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page', 1)
    
    try:
        extra_context['recipes'] = paginator.page(page)
    except PageNotAnInteger:
        extra_context['recipes'] = paginator.page(1)
    except EmptyPage:
        extra_context['recipes'] = paginator.page(paginator.num_pages)

    return render(request, 'cookbook/index.html', extra_context)

def recipes(request):
    extra_context = { }

    extra_context['photo_recipes'] = Recipe.objects.published()[:12]
    recipes = Recipe.objects.published()
    paginator = Paginator(recipes, 6)

    page = request.GET.get('page', 1)
    try:
        extra_context['recipes'] = paginator.page(page)
    except PageNotAnInteger:
        extra_context['recipes'] = paginator.page(1)
    except EmptyPage:
        extra_context['recipes'] = paginator.page(paginator.num_pages)

    extra_context['recipes_only'] = True
    return direct_to_template(request, template='cookbook/recipes.html', extra_context=extra_context)

def top_rated(request):
    extra_context = { }
    extra_context['top_rated'] = True
    extra_context['photo_recipes'] = Recipe.objects.published()[:12]
    recipes = Recipe.objects.order_by("-rating")
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page', 1)
    try:
        extra_context['recipes'] = paginator.page(page)
    except PageNotAnInteger:
        extra_context['recipes'] = paginator.page(1)
    except EmptyPage:
        extra_context['recipes'] = paginator.page(paginator.num_pages)

    return direct_to_template(request, template='cookbook/recipes.html', extra_context=extra_context)

def view_recipe(request, category_slug, recipe_slug):
    extra_context = {}
    extra_context['photo_recipes'] = Recipe.objects.published()[:12]
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    extra_context['recipe'] = recipe
    extra_context['profile'] = recipe.author.get_profile()
    extra_context['related_recipes'] = get_related(recipe.title)

    return render(request, 'cookbook/recipe.html', extra_context)

def tag(request, tag_slug):
    extra_context = {}
    extra_context['photo_recipes'] = Recipe.objects.published()[:12]
    extra_context['recipes_only'] = True
    query_tag = Tag.objects.get(slug=tag_slug)
    extra_context['tag'] = query_tag.name
    recipes = TaggedItem.objects.get_by_model(Recipe, query_tag)
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page', 1)
    try:
        extra_context['recipes'] = paginator.page(page)
    except PageNotAnInteger:
        extra_context['recipes'] = paginator.page(1)
    except EmptyPage:
        extra_context['recipes'] = paginator.page(paginator.num_pages)


    return render(request, 'cookbook/recipes.html', extra_context)


def category(request, category_slug):
    context = {}
    recipes = Recipe.objects.filter(category__slug=category_slug)
    context['category'] = Category.objects.get(slug=category_slug)
    context['recipes'] = recipes
    paginator = Paginator(recipes, 6)
    page = request.GET.get('page', 1)
    try:
        context['recipes'] = paginator.page(page)
    except PageNotAnInteger:
        context['recipes'] = paginator.page(1)
    except EmptyPage:
        context['recipes'] = paginator.page(paginator.num_pages)
    
    return render(request, 'cookbook/recipes.html', context)
    
    

def search(request):
    extra_context = {}
    extra_context['search_query'] = request.GET.get('search')
    search_query = request.GET.get('search')
    extra_context['photo_recipes'] = Recipe.objects.published()[:12]
    extra_context['recipes_only'] = True
    recipes = Recipe.objects.filter(Q(title__icontains=search_query) | Q(directions__icontains=search_query) | Q(ingredients__icontains=search_query))

    paginator = Paginator(recipes, 6)
    page = request.GET.get('page', 1)
    try:
        extra_context['recipes'] = paginator.page(page)
    except PageNotAnInteger:
        extra_context['recipes'] = paginator.page(1)
    except EmptyPage:
        extra_context['recipes'] = paginator.page(paginator.num_pages)



    return direct_to_template(request, template='cookbook/recipes.html', extra_context=extra_context)

@login_required
def add(request):
    
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = RecipeForm()
        extra_context = { }
        extra_context['photo_recipes'] = Recipe.objects.published()[:9]
        extra_context['form'] = form

    return direct_to_template(request, template='cookbook/add.html', extra_context=extra_context)