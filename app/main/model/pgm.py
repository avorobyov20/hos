from django.db import models
from django.utils.safestring import mark_safe
from easy_thumbnails.fields import ThumbnailerImageField
from main.utilities import get_timestamp_path
from main.model.genre import Genre


"""
https://api.hos.com/vo-intro/pgm0984_MT/256k/s00500.ts
https://api.hos.com/vo-intro/pgm0984/256k/s00500.ts
https://ask-dev.ru/info/45711/concatenate-two-mp4-files-using-ffmpeg
"""


class Pgm(models.Model):
    num = models.CharField(
        max_length=4, db_index=True, unique=True, verbose_name="Номер"
    )
    name = models.CharField(
        max_length=48, db_index=True, unique=True, verbose_name="Название"
    )
    date = models.DateField(
        db_index=True, unique=True, verbose_name="Дата выхода в эфир"
    )
    note = models.CharField(
        max_length=177, db_index=True, verbose_name="Описание программы"
    )
    intro = models.TextField(verbose_name="Вступительное слово")
    """
    cover = models.ImageField(
        blank=True, null=True, upload_to=get_timestamp_path,
        verbose_name='1024 x 272'
    )
    """
    cover = ThumbnailerImageField(
        blank=True,
        null=True,
        upload_to=get_timestamp_path,
        verbose_name="1024 x 272",
        resize_source={"size": (200, 0), "crop": "scale"},
    )

    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.num + " " + self.name

    def cover_img(self):
        if self.cover:
            return mark_safe(
                '<img src="{}" width="200" />'.format(self.cover.url)
            )
        else:  # если у программы нет собственной обложки, то...
            gen = (
                self.genres.first()
            )  # получаем первый, привязанный к программе стиль...
            if (
                gen.cover
            ):  # и, если у этого стиля есть обложка, то показываем ее...
                return mark_safe(
                    '<img src="{}"'.format(gen.cover.url)
                    + ' style="width:200px;opacity:0.25;" />'  # полупрозрачной
                )
            else:
                return "no image"

    cover_img.short_description = "Обложка программы"

    class Meta:
        ordering = ("-num",)
        verbose_name_plural = " Программы"
        verbose_name = "Программа"
