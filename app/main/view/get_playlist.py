from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from main.model.playlist import Playlist
from main.model.playlisttracks import PlaylistTracks
from main.models import AdvUser


def get_playlist(request, playlist_pk):
    playlist: Playlist = get_object_or_404(Playlist, pk=playlist_pk)
    user: AdvUser = request.user
    playlist_dict = dict()
    playlist_dict["pk"] = playlist.pk
    playlist_dict["user_pk"] = playlist.user.pk
    playlist_dict["name"] = playlist.name
    playlist_dict["note"] = playlist.note
    playlist_dict["intro"] = playlist.intro
    tracks_list = list()
    for playlisttrack in PlaylistTracks.objects.filter(
        playlist__exact=playlist
    ).all():
        track_dict = dict()
        track_dict["my"] = ""
        if user.is_authenticated:
            if user.username != "admin":
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
                if PlaylistTracks.objects.filter(
                    playlist__exact=playlist1, track__exact=playlisttrack.track
                ).exists():
                    # pos1 <--> my4
                    track_dict[
                        "my"
                    ] = "<span class='hos-my'>&nbsp;4&nbsp;</span> "
                elif PlaylistTracks.objects.filter(
                    playlist__exact=playlist2, track__exact=playlisttrack.track
                ).exists():
                    # pos2 <--> my3
                    track_dict[
                        "my"
                    ] = "<span class='hos-my'>&nbsp;3&nbsp;</span> "
                elif PlaylistTracks.objects.filter(
                    playlist__exact=playlist3, track__exact=playlisttrack.track
                ).exists():
                    # pos3 <--> my2
                    track_dict[
                        "my"
                    ] = "<span class='hos-my'>&nbsp;2&nbsp;</span> "
                elif PlaylistTracks.objects.filter(
                    playlist__exact=playlist4, track__exact=playlisttrack.track
                ).exists():
                    # pos4 <--> my1
                    track_dict[
                        "my"
                    ] = "<span class='hos-my'>&nbsp;1&nbsp;</span> "
                else:
                    track_dict["my"] = "<span class='hos-my'></span> "
        track_dict["artist"] = playlisttrack.track.artist
        track_dict["title"] = playlisttrack.track.title
        track_dict["album"] = playlisttrack.track.album
        track_dict["pgm_num"] = playlisttrack.track.pgm.num
        track_dict["pgm_name"] = playlisttrack.track.pgm.name
        track_dict["cover_url"] = playlisttrack.track.cover.url
        track_dict["duration"] = playlisttrack.track.duration
        # track_dict['duration_str'] = '%02d:%02d' % divmod(track.duration, 60)
        track_dict["get_audio_url"] = playlisttrack.track.get_audio_url()
        tracks_list.append(track_dict)
    playlist_dict["tracks"] = tracks_list
    # элемент in_favs будет в словаре только у авторизованных пользователей
    if user.is_authenticated:
        if user.liked_playlists.filter(pk=playlist.pk).exists():
            playlist_dict["in_favs"] = 1
        else:
            playlist_dict["in_favs"] = 0

    return JsonResponse(playlist_dict)
