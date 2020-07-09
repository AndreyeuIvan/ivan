from django.contrib import admin
from rango.models import Category, Page, Rating, UserProfile


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'url')

admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(UserProfile)