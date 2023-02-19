from django.contrib import admin
from django.utils.safestring import mark_safe
from urllib import parse
from main.model.track import Track


class NumrangeFilter(admin.SimpleListFilter):
    title = "Диапазоны номеров"
    parameter_name = "numrange"

    def lookups(self, request, model_admin):
        return (
            ("1000-1090", "1000 ..."),
            ("0900-0999", "900 - 999"),
            ("0800-0899", "800 - 899"),
            ("0700-0799", "700 - 799"),
            ("0600-0699", "600 - 699"),
            ("0500-0599", "500 - 599"),
            ("0400-0499", "400 - 499"),
            ("0300-0399", "300 - 399"),
            ("0200-0299", "200 - 299"),
            ("0100-0199", "100 - 199"),
            ("0001-0099", "001 - 099"),
        )

    def queryset(self, request, queryset):
        val = str(self.value())
        if "-" in val:
            return queryset.filter(num__startswith=val[:2])
        else:
            return queryset.all()


class PgmAdmin(admin.ModelAdmin):
    fields = (
        "num",
        "name",
        "get_name",
        "get_genres",
        "date",
        "note",
        "intro",
        "cover",
        "cover_img",
        "genres",
    )
    list_display = ("cover_img", "num", "get_name", "get_genres", "note")
    list_display_links = ("num", "cover_img", "note")
    readonly_fields = ("cover_img", "get_name", "get_genres")
    list_per_page = 10
    list_filter = (
        NumrangeFilter,
        "genres__name",
    )
    search_fields = ("num", "name", "note", "intro")
    sortable_by = ("num",)

    filter_horizontal = ("genres",)

    def get_name(self, obj):
        return mark_safe(
            "<a href='/admin/main/track/?all=&"
            + parse.urlencode({"q": obj.name})
            + "+"
            + obj.num
            + "'>"
            + obj.name
            + " ("
            + str(Track.objects.filter(pgm__num__exact=obj.num).count())
            + ")</a>"
        )

    get_name.short_description = "К трекам программы"

    def get_genres(self, obj):
        return mark_safe(
            "<br>".join(
                [
                    "<a href='/admin/main/track/?"
                    + parse.urlencode({"pgm__genres__name": gen.name})
                    + "'>"
                    + gen.name
                    + " ("
                    + str(Track.objects.filter(pgm__genres__exact=gen).count())
                    + ")</a>"
                    for gen in obj.genres.all()
                ]
            )
        )

    get_genres.short_description = "К трекам стиля"

    class Media:
        css = {"all": ("css/PgmAdmin.css",)}
