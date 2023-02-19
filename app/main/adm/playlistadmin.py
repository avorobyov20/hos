from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from adminsortable2.admin import SortableAdminMixin
from main.model.playlist import Playlist
from django.utils.safestring import mark_safe


class TrackTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Playlist.tracks.through
    readonly_fields = (
        "track",
        "get_html_full",
    )
    can_delete = True

    def get_html_full(self, obj):
        return mark_safe(obj.track.get_html_full())

    get_html_full.short_description = ""

    def has_add_permission(self, request, obj=None):
        return False

    class Media:
        css = {"all": ("css/TrackTabularInline.css",)}


class PlaylistAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display_links = ("__str__", "intro", "subrubric", "created_at")
    readonly_fields = ("created_at",)
    sortable_by = []
    inlines = (TrackTabularInline,)
    save_on_top = True

    def get_fields(self, request, obj=None):
        if request.user.username == "admin":
            return ["name", "note", "intro", "subrubric", "created_at"]
        else:
            return ["name", "note", "intro"]

    def get_list_display(self, request):
        if request.user.username == "admin":
            return ["__str__", "intro", "subrubric", "created_at"]
        else:
            return ["__str__", "intro"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
