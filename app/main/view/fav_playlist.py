from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from main.model.playlist import Playlist


def fav_playlist(request, playlist_pk):
    playlist: Playlist = get_object_or_404(Playlist, pk=playlist_pk)
    try:
        if request.user.liked_playlists.filter(pk=playlist.pk).exists():
            request.user.liked_playlists.remove(playlist)
        else:
            request.user.liked_playlists.add(playlist)
    except Exception:  # если что-то пошло не так, возвращаем False
        return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 1})
