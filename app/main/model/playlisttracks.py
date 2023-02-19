from django.db import models
from main.model.playlist import Playlist
from main.model.track import Track


class PlaylistTracks(models.Model):
    playlist = models.ForeignKey(
        Playlist, on_delete=models.CASCADE
    )  # при удалении плейлиста чистится кросс-таблица
    track = models.ForeignKey(
        Track, on_delete=models.CASCADE
    )  # при удалении трека чистится кросс
    track_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s.%02d~ %s // %s / %s -- %s -- " % (
            self.track.pgm.num,
            self.track.pos,
            self.track.pgm.name,
            self.track.artist,
            self.track.album,
            self.track.title,
        ) + "%02d:%02d" % divmod(self.track.duration, 60)

    class Meta:
        ordering = ["track_order"]
        verbose_name_plural = "Треки"
        verbose_name = "Трек"
