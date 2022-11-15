# from django.contrib import admin
# from .models import Post
# admin.site.register(Post)
from django.contrib import admin
from .models import *


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'user_rate')
    list_display_links = ('id', 'author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'article_category',)
    list_display_links = ('id', 'article_category',)
    list_filter = ('article_category',)
    save_as = True


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'post_author', 'date_created', 'post_rate')
    list_display_links = ('id', 'title',)
    list_filter = ('category',)
    search_fields = ('title',)
    inlines = [CommentInlineAdmin]
    save_on_top = True
    save_as = True
    list_editable = ('category',)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_category')
    list_display_links = ('id', 'post_category',)


@admin.register(Comment)
class CommentAdminInline(admin.ModelAdmin):
    list_display = ('id', 'comment_post', 'comment_user', 'comment_date_created', 'comment_rate')
    list_display_links = ('id', 'comment_post',)
