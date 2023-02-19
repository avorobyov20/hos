from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe
from urllib import parse
from main.model.genre import Genre
from main.model.track import Track


class FrequencyFilter(admin.SimpleListFilter):
    title = "Присутствие в эфире"
    parameter_name = "freq"

    def lookups(self, request, model_admin):
        return (
            ("constantly", "Постоянно"),
            ("often", "Часто"),
            ("sometimes", "Иногда"),
            ("rarely", "Редко"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == "constantly":
            return queryset.filter(pgm_count__gt=70)
        elif val == "often":
            return queryset.filter(pgm_count__lte=70, pgm_count__gt=35)
        elif val == "sometimes":
            return queryset.filter(pgm_count__lte=35, pgm_count__gt=13)
        elif val == "rarely":
            return queryset.filter(pgm_count__lte=13)


# https://stackoverflow.com/questions/20732660/change-the-column-width-in-the-django-admin-panel
class GenreAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "get_pgm_count",
        "get_track_count",
        "is_free_count",
        "cover",
        "cover_img",
    )
    list_display = (
        "cover_img",
        "name",
        "get_pgm_count",
        "get_track_count",
        "is_free_count",
    )
    list_display_links = (
        "cover_img",
        "name",
    )
    list_filter = (FrequencyFilter,)
    sortable_by = ()
    search_fields = ("name",)
    readonly_fields = (
        "cover_img",
        "get_pgm_count",
        "get_track_count",
        "is_free_count",
    )
    list_per_page = 10

    def get_ordering(self, request):
        return ["name"]

    def get_queryset(self, request):
        return Genre.objects.annotate(pgm_count=Count("pgm"))

    def get_pgm_count(self, obj):
        # функциональное поле, количество программ...
        return mark_safe(
            "<a href='/admin/main/pgm/?"
            + parse.urlencode({"genres__name": obj.name})
            + "'>"
            + str(obj.pgm_set.count())
            + "</a>"
        )

    get_pgm_count.short_description = "К программам"  # ...относящихся к стилю
    get_pgm_count.admin_order_field = "pgm_count"

    def get_track_count(self, obj):
        # функциональное поле, количество треков...
        return mark_safe(
            "<a href='/admin/main/track/?"
            + parse.urlencode({"pgm__genres__name": obj.name})
            + "'>"
            + str(
                Track.objects.filter(pgm__genres__name__exact=obj.name).count()
            )
            + "</a>"
        )

    get_track_count.short_description = "К трекам"  # ...относящихся к стилю

    def is_free_count(self, obj):
        return mark_safe(
            "<a href='/admin/main/track/?is_free__exact=1&"
            + parse.urlencode({"pgm__genres__name": obj.name})
            + "'>"
            + str(
                Track.objects.filter(pgm__genres__exact=obj.pk)
                .filter(is_free__exact=True)
                .count()
            )
            + "</a>"
        )

    is_free_count.short_description = (
        "К свободным трекам"  # количество треков без Content ID
    )

    class Media:
        css = {"all": ("css/GenreAdmin.css",)}
