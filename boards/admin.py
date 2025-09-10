from django.contrib import admin
from .models import Board, Topic, Post
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

admin.site.unregister(Group)

class InlineTopic(admin.TabularInline):
    model = Topic
    extra = 1

class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    inlines = [InlineTopic]

admin.site.register(Board, BoardAdmin)

class TopicAdmin(ImportExportModelAdmin):
    list_display = ('title', 'board', 'created_at', 'created_by')
    search_fields = ('title', 'board__name')

admin.site.register(Topic, TopicAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'created_by', 'created_at', 'updated_at', 'combined_topic_and_user')
    search_fields = ('topic__title', 'created_by__username')

    def combined_topic_and_user(self, obj):
        return f"{obj.topic.title} - {obj.created_by.username}"
    combined_topic_and_user.short_description = "Combined Topic and User"

admin.site.register(Post, PostAdmin)