from django.contrib import admin
from django.utils.safestring import mark_safe

from django import forms
from .models import Category, Genre, Movie, MovieShots, Actor, Reviews
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    list_display_links = ("name",)


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=auto height=100px')

    get_image.short_description = "Photo"


class ReviewInLine(admin.TabularInline):
    model = Reviews
    readonly_fields = ("name", "email")
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    list_editable = ("draft",)
    inlines = [MovieShotsInLine, ReviewInLine]
    save_on_top = True
    save_as = True
    readonly_fields = ("get_image",)
    actions = ["publish", "unpublish"]

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width=auto height=450px')

    get_image.short_description = "Poster"

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 record was refreshed"
        else:
            message_bit = f"{row_update} records were refreshed"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 record was refreshed"
        else:
            message_bit = f"{row_update} records were refreshed"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ('change',)
    unpublish.short_description = "Unpublish"
    unpublish.allowed_permissions = ('change',)


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=auto height=100px')

    get_image.short_description = "Photo"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")

    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width=auto height=100px')

    get_image.short_description = "Photo"


# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(Actor)
# admin.site.register(Reviews)

admin.site.site_title = "MovieSet Admin"
admin.site.site_header = "MovieSet Admin"
