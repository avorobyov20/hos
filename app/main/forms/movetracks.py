from django import forms
from main.model.playlist import Playlist
from main.model.rubric import SubRubric


# https://stackoverflow.com/questions/15608784/django-filter-the-queryset-of-modelchoicefield
class MoveTracksToPlaylistForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    playlist = forms.ModelChoiceField(
        queryset=Playlist.objects.none(),
    )


class MoveTracksToNewPlaylistForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    new_playlist_name = forms.CharField(
        required=True, max_length=48, label="Название плейлиста"
    )
    new_playlist_note = forms.CharField(
        required=False, max_length=177, label="Описание"
    )
    new_playlist_subrubric = forms.ModelChoiceField(
        queryset=SubRubric.objects, label="Подрубрика"
    )
