from django.db import models
from django.utils.safestring import mark_safe
from easy_thumbnails.fields import ThumbnailerImageField
from main.model.pgm import Pgm
from urllib import parse
from django_project.settings import AAC_URL_PREFIX


class Track(models.Model):
    pos = models.SmallIntegerField(db_index=True, verbose_name="Трек")
    artist = models.CharField(
        max_length=77, db_index=True, verbose_name="Исполнитель"
    )
    album = models.CharField(
        max_length=103, db_index=True, verbose_name="Альбом"
    )
    title = models.CharField(
        max_length=93, db_index=True, verbose_name="Название"
    )
    label = models.CharField(
        max_length=51,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="Лейбл",
    )
    duration = models.SmallIntegerField(
        db_index=True, verbose_name="Длительность, сек."
    )
    is_free = models.BooleanField(
        db_index=True, default=False, verbose_name="Free"
    )
    year = models.SmallIntegerField(
        db_index=True, null=True, blank=True, verbose_name="Год"
    )
    pgm = models.ForeignKey(
        Pgm, on_delete=models.PROTECT, verbose_name="Программа"
    )
    cover = ThumbnailerImageField(
        blank=True,
        null=True,
        verbose_name="1 x 1, png",
        resize_source={"size": (80, 80), "crop": "scale"},
    )

    def get_pgmnum(self, showgenres=True):
        if self.is_free:
            free = (
                "<span style='color: white; background-color: "
                + "rgba(112, 191, 43, 0.5);'>&nbsp;FREE&nbsp;</span>"
            )
        else:
            free = (
                "<span style='color:white; background-color: "
                + "rgba(221, 70, 70, 0.22);'>&nbsp;Content ID&nbsp;</span>"
            )
        if showgenres:
            gens_str = "<br>" + "<br>".join(
                [
                    "<a href='/admin/main/pgm/?"
                    + parse.urlencode({"genres__name": gen.name})
                    + "'>"
                    + gen.name
                    + " ("
                    + str(Pgm.objects.filter(genres__exact=gen).count())
                    + ")</a>"
                    for gen in self.pgm.genres.all()
                ]
            )
        else:
            gens_str = ""
        return (
            "<a href='/admin/main/track/?all=&"
            + parse.urlencode({"q": self.pgm.name})
            + "+"
            + self.pgm.num
            + "'>"
            + self.pgm.name
            + "</a><br>"
            + free
            + "<br>"
            + "<span style='color: #447e9b;'>%02d</span> " % (self.pos,)
            + "<a href='/admin/main/pgm/"
            + self.pgm.num
            + "/change/'>~"
            + self.pgm.num
            + "</a>"
            + gens_str
        )

    def get_audio_url(self):
        return AAC_URL_PREFIX + "/aac/%s.%02d.m4a" % (self.pgm.num, self.pos)

    def get_audio(self):
        return (
            '<div style="background-image: url({}); '.format(self.cover.url)
            + 'width: 80px; height: 80px; background-size: cover;">'
            + '<audio controls preload="none" '
            + 'class="iru-tiny-player" data-title=" ">'
            + '<source src="'
            + AAC_URL_PREFIX
            + '/aac/%s.%02d.m4a" type="audio/mpeg"></audio></div>'
            % (self.pgm.num, self.pos)
        )

    def get_duration(self):
        return '<br><br><div style="">%02d:%02d</div>' % divmod(
            self.duration, 60
        )

    def get_aat(self, showyear=True, showlabel=True):
        res = (
            "<a href='/admin/main/track/?"
            + parse.urlencode({"q": self.artist})
            + "'>"
            + self.artist
            + "</a><br>"
            + "<a href='/admin/main/track/?"
            + parse.urlencode({"q": self.album})
            + "'>"
            + self.album
            + "</a><br>"
            + "<a href='/admin/main/track/?"
            + parse.urlencode({"q": self.title})
            + "'>"
            + self.title
            + "</a><br>"
        )
        if showyear:
            if self.year:
                res = (
                    "<span style='color: #666; background-color: #f8f8f8;'>"
                    + str(self.year)
                    + "</span><br>"
                    + res
                )
            else:
                res = (
                    "<span style='color:transparent;"
                    + "background-color: #f8f8f8;'>&nbsp;0000&nbsp;</span>"
                    + "<br>"
                    + res
                )
        if showlabel:
            if self.label:
                res += (
                    "<span style='color: #666; background-color: #f8f8f8;'>"
                    + self.label
                    + "</span>"
                )
            else:
                res += (
                    "<span style='color: transparent; "
                    + "background-color: #f8f8f8;'>"
                    + "&nbsp;unknown&nbsp;</span>"
                )
        return res

    def get_html_full(self):
        return (
            "<div style='overflow: hidden;'><div style='width: 1000%;'>"
            + "<div style='float: left; width: 200px; height: 80px;'>%s</div>"
            % self.get_pgmnum(showgenres=False)
            + "<div style='float: left; width: 95px; height: 80px;'>%s</div>"
            % self.get_audio()
            + "<div style='float: left; width: 45px; height: 80px; "
            + "color: #447e9b;' >%02d:%02d</div>" % divmod(self.duration, 60)
            + "<div style='float:left;"
            + "width: 255px; height: 80px;'>%s</div></div></div>"
            % self.get_aat(showyear=False, showlabel=False)
        )

    def get_html_full_safe(self):
        return mark_safe(self.get_html_full())

    def __str__(self):
        return ""

    def cover_img(self):
        if self.cover:
            return mark_safe(
                '<img src="{}" width="80" />'.format(self.cover.url)
            )
        else:
            return mark_safe("нет картинки")

    cover_img.short_description = "Обложка альбома"

    class Meta:
        ordering = (
            "-pgm__num",
            "pos",
        )
        verbose_name_plural = " Треки программ"
        verbose_name = "Трек программы"
