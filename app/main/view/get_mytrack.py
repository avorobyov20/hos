from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from main.model.pgm import Pgm
from main.model.track import Track
from main.model.playlist import Playlist
from main.model.playlisttracks import PlaylistTracks
from main.models import AdvUser


def get_mytrack(request, pgm_num, track_pos):
    user: AdvUser = request.user
    if not user.is_authenticated:
        return JsonResponse({"id": "0"})
    elif user.username == "admin":
        return JsonResponse({"id": "0"})
    else:
        pgm: Pgm = get_object_or_404(Pgm, num__exact=pgm_num)
        track: Track = get_object_or_404(
            Track, pgm__exact=pgm, pos__exact=track_pos
        )
        playlist1: Playlist = Playlist.objects.get(
            user__exact=user, subrubric__name__exact="#", pos__exact=1
        )
        cnt1 = PlaylistTracks.objects.filter(playlist__exact=playlist1).count()
        playlist2: Playlist = Playlist.objects.get(
            user__exact=user, subrubric__name__exact="#", pos__exact=2
        )
        cnt2 = PlaylistTracks.objects.filter(playlist__exact=playlist2).count()
        playlist3: Playlist = Playlist.objects.get(
            user__exact=user, subrubric__name__exact="#", pos__exact=3
        )
        cnt3 = PlaylistTracks.objects.filter(playlist__exact=playlist3).count()
        playlist4: Playlist = Playlist.objects.get(
            user__exact=user, subrubric__name__exact="#", pos__exact=4
        )
        cnt4 = PlaylistTracks.objects.filter(playlist__exact=playlist4).count()
        if PlaylistTracks.objects.filter(
            playlist__exact=playlist1, track__exact=track
        ).exists():
            return JsonResponse(
                {
                    "id": "my1",
                    "playlist_pk_" + str(playlist1.pk): cnt1,
                    "playlist_pk_" + str(playlist2.pk): cnt2,
                    "playlist_pk_" + str(playlist3.pk): cnt3,
                    "playlist_pk_" + str(playlist4.pk): cnt4,
                }
            )
        if PlaylistTracks.objects.filter(
            playlist__exact=playlist2, track__exact=track
        ).exists():
            return JsonResponse(
                {
                    "id": "my2",
                    "playlist_pk_" + str(playlist1.pk): cnt1,
                    "playlist_pk_" + str(playlist2.pk): cnt2,
                    "playlist_pk_" + str(playlist3.pk): cnt3,
                    "playlist_pk_" + str(playlist4.pk): cnt4,
                }
            )
        if PlaylistTracks.objects.filter(
            playlist__exact=playlist3, track__exact=track
        ).exists():
            return JsonResponse(
                {
                    "id": "my3",
                    "playlist_pk_" + str(playlist1.pk): cnt1,
                    "playlist_pk_" + str(playlist2.pk): cnt2,
                    "playlist_pk_" + str(playlist3.pk): cnt3,
                    "playlist_pk_" + str(playlist4.pk): cnt4,
                }
            )
        if PlaylistTracks.objects.filter(
            playlist__exact=playlist4, track__exact=track
        ).exists():
            return JsonResponse(
                {
                    "id": "my4",
                    "playlist_pk_" + str(playlist1.pk): cnt1,
                    "playlist_pk_" + str(playlist2.pk): cnt2,
                    "playlist_pk_" + str(playlist3.pk): cnt3,
                    "playlist_pk_" + str(playlist4.pk): cnt4,
                }
            )
        return JsonResponse(
            {
                "id": "my0",
                "playlist_pk_" + str(playlist1.pk): cnt1,
                "playlist_pk_" + str(playlist2.pk): cnt2,
                "playlist_pk_" + str(playlist3.pk): cnt3,
                "playlist_pk_" + str(playlist4.pk): cnt4,
            }
        )
