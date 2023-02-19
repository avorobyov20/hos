from django.contrib import admin

from .models import AdvUser
from main.model.genre import Genre
from main.model.pgm import Pgm
from main.model.track import Track
from main.model.playlist import Playlist
from main.model.rubric import SuperRubric, SubRubric

from main.adm.advuseradmin import AdvUserAdmin
from main.adm.genreadmin import GenreAdmin
from main.adm.pgmadmin import PgmAdmin
from main.adm.trackadmin import TrackAdmin
from main.adm.playlistadmin import PlaylistAdmin
from main.adm.rubricadmin import SuperRubricAdmin, SubRubricAdmin

admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Pgm, PgmAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Playlist, PlaylistAdmin)

admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
