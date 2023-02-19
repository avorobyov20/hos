from django.contrib import admin
from django.db.models.functions import Substr, Cast
from django.utils.safestring import mark_safe
from django.db.models import SmallIntegerField
from main.forms.movetracks import MoveTracksToPlaylistForm
from main.forms.movetracks import MoveTracksToNewPlaylistForm
from main.model.playlist import Playlist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
import datetime
from main.model.playlisttracks import PlaylistTracks


class TrackNumrangeABFilter(admin.SimpleListFilter):
    title = "Сотни"
    parameter_name = "ab"

    def lookups(self, request, model_admin):
        return (
            ("10--", "10--"),
            ("09--", "09--"),
            ("08--", "08--"),
            ("07--", "07--"),
            ("06--", "06--"),
            ("05--", "05--"),
            ("04--", "04--"),
            ("03--", "03--"),
            ("02--", "02--"),
            ("01--", "01--"),
            ("00--", "00--"),
        )

    def queryset(self, request, queryset):
        val = str(self.value())
        if "--" in val:
            return queryset.filter(pgm__num__startswith=val[:2])
        else:
            return queryset.all()


class TrackNumrangeCDFilter(admin.SimpleListFilter):
    title = "Десятки"
    parameter_name = "cd"

    def lookups(self, request, model_admin):
        return (
            ("--9-", "--9-"),
            ("--8-", "--8-"),
            ("--7-", "--7-"),
            ("--6-", "--6-"),
            ("--5-", "--5-"),
            ("--4-", "--4-"),
            ("--3-", "--3-"),
            ("--2-", "--2-"),
            ("--1-", "--1-"),
            ("--0-", "--0-"),
        )

    def queryset(self, request, queryset):
        val = str(self.value())
        if "--" in val:
            i = 10 * int(val[2:3])
            return queryset.annotate(
                cd=Cast(Substr("pgm__num", 3, 2), SmallIntegerField())
            ).filter(cd__range=(i, i + 9))
        else:
            return queryset.all()


def move_tracks_to_playlist(modeladmin, request, queryset):
    form = None
    if "apply" in request.POST:
        form = MoveTracksToPlaylistForm(request.POST)
        form.fields["playlist"].queryset = Playlist.objects.filter(
            user=request.user
        )
        if form.is_valid():
            playlist = form.cleaned_data["playlist"]
            count = 0
            for track in queryset:
                if not track.playlist_set.filter(pk=playlist.pk).exists():
                    playlist.tracks.add(track)
                count += 1
            modeladmin.message_user(
                request,
                mark_safe(
                    "%d треков успешно добавлены в плейлист " % (count,)
                    + "<a href='/admin/main/playlist/%d/change/'>%s</a>"
                    % (playlist.pk, playlist)
                ),
            )
            return HttpResponseRedirect(request.get_full_path())
    if not form:
        form = MoveTracksToPlaylistForm(
            initial={
                "_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME)
            }
        )
        form.fields["playlist"].queryset = Playlist.objects.filter(
            user=request.user
        )
    return render(
        request,
        "admin/move_tracks_to_playlist.html",
        {
            "tracks": queryset,
            "form": form,
            "title": "Добавление треков в плейлист",
        },
    )


move_tracks_to_playlist.short_description = "Добавить треки в плейлист"


def move_tracks_to_new_playlist(modeladmin, request, queryset):
    form = None
    if "apply" in request.POST:
        form = MoveTracksToNewPlaylistForm(request.POST)
        if form.is_valid():
            new_playlist_name = form.cleaned_data["new_playlist_name"]
            new_playlist_note = form.cleaned_data["new_playlist_note"]
            new_playlist_subrubric = form.cleaned_data[
                "new_playlist_subrubric"
            ]
            if (
                Playlist.objects.filter(user__exact=request.user)
                .filter(name__exact=new_playlist_name)
                .exists()
            ):
                new_playlist_name += " %s" % (
                    datetime.datetime.now().timestamp(),
                )
            playlist = Playlist(
                user=request.user,
                name=new_playlist_name,
                note=new_playlist_note,
                subrubric=new_playlist_subrubric,
            )
            playlist.save()
            count = 0
            for track in queryset:
                PlaylistTracks(
                    playlist=playlist, track=track
                ).save()  # playlist.tracks.add(track)
                count += 1
            modeladmin.message_user(
                request,
                mark_safe(
                    "%d треков успешно добавлены в новый плейлист " % (count,)
                    + "<a href='/admin/main/playlist/%d/change/'>%s</a>"
                    % (playlist.pk, playlist)
                ),
            )
            return HttpResponseRedirect(request.get_full_path())
    if not form:
        form = MoveTracksToNewPlaylistForm(
            initial={
                "_selected_action": request.POST.getlist(ACTION_CHECKBOX_NAME),
                "new_playlist_name": request.GET.get("q"),
            }
        )
    return render(
        request,
        "admin/move_tracks_to_new_playlist.html",
        {
            "tracks": queryset,
            "form": form,
            "title": "Добавление треков в новый плейлист",
        },
    )


move_tracks_to_new_playlist.short_description = (
    "Добавить треки в новый плейлист"
)


class TrackAdmin(admin.ModelAdmin):
    fields = (
        "pgm",
        "pos",
        ("cover_img", "cover"),
        "artist",
        "album",
        "title",
        ("duration", "is_free"),
        ("year", "label"),
    )
    list_display = (
        "get_pgmnum",
        "get_audio",
        "get_duration",
        "get_aat",
    )
    list_display_links = ("get_duration",)
    readonly_fields = ("cover_img",)
    list_per_page = 7
    search_fields = (
        "artist",
        "album",
        "title",
        "pgm__num",
        "pgm__name",
    )
    sortable_by = ()
    list_filter = (
        TrackNumrangeABFilter,
        TrackNumrangeCDFilter,
        "pgm__genres__name",
        "is_free",
    )
    actions = (
        move_tracks_to_playlist,
        move_tracks_to_new_playlist,
    )  # вызовем функцию move_tracks_to_playlist

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username != "admin":
            del actions[
                "move_tracks_to_new_playlist"
            ]  # у простых пользователей не должно быть такой возможности
        return actions

    def get_audio(self, obj):
        return mark_safe(obj.get_audio())

    get_audio.short_description = "Источник"

    def get_duration(self, obj):
        return mark_safe(obj.get_duration())

    get_duration.admin_order_field = "duration"
    get_duration.short_description = "Edit"

    def get_pgmnum(self, obj):
        return mark_safe(obj.get_pgmnum())

    get_pgmnum.admin_order_field = "pgm__num"
    get_pgmnum.short_description = "Трек программы"

    def get_aat(self, obj):
        return mark_safe(obj.get_aat())

    get_aat.short_description = "Подробности"

    class Media:
        css = {"all": ("css/TrackAdmin.css",)}
