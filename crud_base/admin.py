from django.contrib import admin
from .models import KnowledgeBase
# Register your models here.


class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)
    search_fields = ['title', 'content']


admin.site.register(KnowledgeBase, KnowledgeBaseAdmin)
