from django.db import models
from django.utils.safestring import mark_safe
from easy_thumbnails.fields import ThumbnailerImageField
from main.utilities import get_timestamp_path


class Genre(models.Model):
    name = models.CharField(
        max_length=28, db_index=True, unique=True, verbose_name="Название"
    )
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

    def __str__(self):
        return self.name

    def cover_img(self):
        if self.cover:
            return mark_safe(
                '<img src="{}" width="200" />'.format(self.cover.url)
            )
        else:
            return mark_safe("нет картинки")

    cover_img.short_description = "Обложка стиля"

    class Meta:
        verbose_name_plural = " Музыкальные стили"
        verbose_name = "Музыкальный стиль"
