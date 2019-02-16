from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from django_summernote.admin import SummernoteModelAdmin
from lxml.html.clean import Cleaner

from django.core.exceptions import ObjectDoesNotExist

from .models import *


admin.site.site_header = 'Notícias - Administração'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Gestor'


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 50


class AuthorInline(admin.StackedInline):
    model = Author
    can_delete = False


class ProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login')
    inlines = (AuthorInline, )
    list_per_page = 50

admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'first_name', 'last_name', 'position', 'about')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'fk_position__name', 'about')
    raw_id_fields = ('user',)
    list_per_page = 50


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_per_page = 50


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 50


class ArticleTagInline(admin.StackedInline):
    model = ArticleTag


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'category', 'event_datetime', 'publish_datetime', 'update_datetime')
    search_fields = ('title', 'description', 'fk_author__user__username', 'fk_author__user__first_name', 'fk_author__user__last_name')
    list_filter = ('fk_category__name', 'event_datetime', 'publish_datetime', 'update_datetime')
    raw_id_fields = ('fk_author', 'fk_category')
    inlines = (ArticleTagInline,)
    list_per_page = 50
    summernote_fields = ('content',)
    disableResizeEditor = False

    @staticmethod
    def html_sanitizer(content):
        """ sanitize malicious scripts """
        cleaner = Cleaner()
        cleaner.embedded = False
        cleaner.safe_attrs_only = False
        return cleaner.clean_html(content)

    def get_queryset(self, request):
        articles = super().get_queryset(request)
        if request.user.is_superuser or request.user.has_perm('portal.change_from_another_author'):
            return articles
        return articles.filter(fk_author__user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser or not request.user.has_perm('portal.change_authorship'):
            self.readonly_fields = ('fk_author',)

        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.has_perm('portal.change_authorship'):
            try:
                Author.objects.get(user=request.user.pk)
            except ObjectDoesNotExist:
                pass
            else:
                obj.fk_author = request.user.author

        """ save the sanitized html """
        obj.content = self.html_sanitizer(obj.content)
        super().save_model(request, obj, form, change)


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag')
    search_fields = ('fk_article__title', 'fk_tag__name')
    list_filter = ('fk_tag__name',)
    raw_id_fields = ('fk_article', 'fk_tag')
    list_per_page = 50

    def get_queryset(self, request):
        article_tags = super().get_queryset(request)
        if request.user.is_superuser:
            return article_tags
        return article_tags.filter(fk_article__fk_author__user=request.user)


