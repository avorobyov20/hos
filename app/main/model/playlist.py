from django.db import models
from main.models import AdvUser
from main.model.track import Track
from main.model.rubric import SubRubric
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django_project.settings import PUBLIC_GROUP_ID


class Playlist(models.Model):
    # при удалении пользователя удаляются все его плейлисты
    user = models.ForeignKey(
        AdvUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    subrubric = models.ForeignKey(
        SubRubric,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Подрубрика",
    )  # защитим от удаления
    # позиция плейлиста в списке плейлистов пользователя
    pos = models.PositiveIntegerField(
        default=0, db_index=True, blank=False, null=False, verbose_name="Номер"
    )
    name = models.CharField(
        max_length=53, blank=False, null=False, verbose_name="Название"
    )
    note = models.CharField(
        max_length=177, blank=True, null=True, verbose_name="Описание"
    )
    intro = models.TextField(blank=True, null=True, verbose_name="Вступление")
    tracks = models.ManyToManyField(Track, through="PlaylistTracks")
    favs = models.ManyToManyField(AdvUser, related_name="liked_playlists")

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Опубликован"
    )

    def __str__(self):
        return "%s (%d)" % (self.name, self.playlisttracks_set.count())

    # def get_absolute_url(self):
    #    return "/playlist/%s/" % self.pk

    def get_cover(self):
        trs = self.tracks
        if trs:  # 1. если плейлист не пуст
            gens = trs.first().pgm.genres
            if (
                gens
            ):  # 2. если заполнены жанры у программы к кот относится перв трек
                gen = gens.first()  # берем первый жанр
                if (
                    gen.cover
                ):  # 3. и если у него есть картинка, то возвращаем ее
                    return gen.cover
        else:
            return None

    # пока используется только в шаблоне на главной странице сайта
    get_cover.short_description = "Обложка плейлиста"

    class Meta:
        ordering = ["pos"]
        unique_together = (("user", "name"),)
        index_together = (("user", "name"),)
        verbose_name_plural = "Мои плейлисты"
        verbose_name = "Плейлист"


# Создадим обработчик сигнала pre_save, который принудительно будет назначать
# подрубрику "#" каждому только что созданному пользовательскому плейлисту
# и каждому админскому плейлисту, если админ не указал подрубрику явно
def assign_subrubric_to_users_playlist(sender, instance, **kwargs):
    if instance.user.username != "admin":
        instance.subrubric = SubRubric.objects.get(name="#")
    else:
        if instance.subrubric is None:
            instance.subrubric = SubRubric.objects.get(name="#")


pre_save.connect(assign_subrubric_to_users_playlist, sender=Playlist)


# Создадим обработчик сигнала post_save, который будет настраивать права
# каждому, только что созданному "простому" пользователю
def add_user_to_public_group(sender, instance, created, **kwargs):
    """Post-create user signal that adds the user to everyone group."""

    try:
        if created and instance.username != "admin":
            instance.groups.add(
                Group.objects.get(pk=PUBLIC_GROUP_ID)
            )  # добавляем пользователя в специальную группу
            instance.is_staff = True  # даем доступ к админке
            for i in range(4):  # и создаем 4 плейлиста
                Playlist(
                    user=instance, pos=4 - i, name="my playlist " + str(i + 1)
                ).save()
    except Group.DoesNotExist:
        pass


post_save.connect(add_user_to_public_group, sender=AdvUser)
