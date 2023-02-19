from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from main.model.pgm import Pgm
from main.model.track import Track
from main.model.playlist import Playlist
from main.model.playlisttracks import PlaylistTracks
from main.models import AdvUser


def set_mytrack(request, pgm_num, track_pos, id):
    user: AdvUser = request.user
    if user.is_authenticated:
        if user.username != "admin":
            pgm: Pgm = get_object_or_404(Pgm, num__exact=pgm_num)
            track: Track = get_object_or_404(
                Track, pgm__exact=pgm, pos__exact=track_pos
            )

            playlist1: Playlist = Playlist.objects.get(
                user__exact=user, subrubric__name__exact="#", pos__exact=1
            )
            playlist2: Playlist = Playlist.objects.get(
                user__exact=user, subrubric__name__exact="#", pos__exact=2
            )
            playlist3: Playlist = Playlist.objects.get(
                user__exact=user, subrubric__name__exact="#", pos__exact=3
            )
            playlist4: Playlist = Playlist.objects.get(
                user__exact=user, subrubric__name__exact="#", pos__exact=4
            )

            # удаляем трек из всех пользовательских листов
            PlaylistTracks.objects.filter(
                playlist__in=(playlist1, playlist2, playlist3, playlist4),
                track__exact=track,
            ).delete()
            if id != "my0":
                if int(id[-1:]) == 1:
                    playlist1.tracks.add(track)
                if int(id[-1:]) == 2:
                    playlist2.tracks.add(track)
                if int(id[-1:]) == 3:
                    playlist3.tracks.add(track)
                if int(id[-1:]) == 4:
                    playlist4.tracks.add(track)

            cnt1 = PlaylistTracks.objects.filter(
                playlist__exact=playlist1
            ).count()
            cnt2 = PlaylistTracks.objects.filter(
                playlist__exact=playlist2
            ).count()
            cnt3 = PlaylistTracks.objects.filter(
                playlist__exact=playlist3
            ).count()
            cnt4 = PlaylistTracks.objects.filter(
                playlist__exact=playlist4
            ).count()
            return JsonResponse(
                {
                    "status": 1,
                    "playlist_pk_"
                    + str(playlist1.pk): playlist1.name
                    + " ("
                    + str(cnt1)
                    + ")",
                    "playlist_pk_"
                    + str(playlist2.pk): playlist2.name
                    + " ("
                    + str(cnt2)
                    + ")",
                    "playlist_pk_"
                    + str(playlist3.pk): playlist3.name
                    + " ("
                    + str(cnt3)
                    + ")",
                    "playlist_pk_"
                    + str(playlist4.pk): playlist4.name
                    + " ("
                    + str(cnt4)
                    + ")",
                }
            )
    return JsonResponse(
        {"status": 0}
    )  # для неавторизованного пользователя возвращаем ноль
