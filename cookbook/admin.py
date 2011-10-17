from django.contrib import admin
from cookbook.models import *
from django import forms

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'tags', 'category', 'featured', 'published')
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'ckeditor'})}, }
    save_on_top = True
    
    actions = ['bulk_publish', 'feature']
    
    def bulk_publish(self, request, queryset):
        rows_updated = queryset.update(published=True)
        if rows_updated ==1:
            message_bit = "1 recipe was"
        else:
            message_bit = "%s recipes were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    def feature(self, request, queryset):
        rows_updated = queryset.update(featured=True)
        if rows_updated == 1:
            message_bit = "1 recipe was"
        else:
            message_bit = "%s recipes were" % rows_updated
        self.message_user(request, "%s successfully marked as featured." % message_bit)
        
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    class Media:
        js = ('http://static.derekandlindy.com/staging/cookbook/javascript/ckeditor/ckeditor.js',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'published')
    
    actions = ['publish']
    
    def publish(self, request, queryset):
        rows = queryset.update(published=True)
        if rows == 1:
            message_bit = "1 recipe was"
        else:
            message_bit = "%s recipes were" % rows
        self.message_user(request, "%s successfully published." % message_bit)
        

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile)
