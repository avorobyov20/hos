from django.db import models
from main.model import playlist

"""
RECENT PROGRAMS -- Recently Aired Programs
Electronic
    ELECTRONIC SPACE -- Classic electronic space music
    AMBIENT/DOWNTEMPO -- Spaced-out beats
Ethnic
    CELTIC SPACE -- Celtic space music from the Emerald Isle
    AMBIENT WORLD MIX -- Pan-ethnic and cross-cultural
Other
    SEASONAL -- Music for this Special Season
    CONTEMPORARY/INSTRUMENTAL -- Acoustic and hybrids
    ORCHESTRAL/CHAMBER/CHORAL -- Contemplative classical
    PEACE, BE STILL -- Music to calm the heart and mind
Mix
    ALL ARCHIVE MIX -- Selections from all categories
    CLASSIC HOS MIX -- Acoustic and electronic

Rubric - базовая модель, в которой будут храниться и надрубрики и подрубрики.
Мы создадим две производные от нее прокси-модели: SuperRubric и SubRubric
"""


class Rubric(models.Model):
    name = models.CharField(
        max_length=25, db_index=True, unique=True, verbose_name="Название"
    )
    note = models.CharField(
        max_length=40,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Описание",
    )
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    super_rubric = models.ForeignKey(
        "SuperRubric",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Надрубрика",
    )  # необязательное, запрет каскадного удаления

    # Связь, создаваемая этим полем, должна устанавливаться
    # с моделью SuperRubric. Это поле будет заполняться только в том случае,
    # если запись хранит подрубрику. Связать подрубрику можно только
    # с суперрубрикой, т.е. рубрикой, у которой это поле будет пустым.
    # Нужно обязательно запретить каскадное удаление. Если этого не сделать,
    # то пользователь по ошибке удалит какую-нибудь суперрубрику со всеми ее
    # подрубриками. Никакие параметры этой модели не задаем, поскольку
    # пользователи не будут работать с ней непосредственно.

    class Meta:
        ordering = ("order",)


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SubRubricManager(models.Manager):
    # пока не понятно как сделать, чтобы "UNCATEGORIZED" не появлялся в адмике
    # скорее всего, эту строку вообще не нужно добавлять в справочник
    def get_queryset(self):
        return (
            super().get_queryset().filter(super_rubric__isnull=False)
        )  # единственное отличие от SuperRubric


# Для работы с надрубриками объявим прокси-модель SuperRubric
# (здесь "прокси" подразумевает изменение функциональности производной модели
# при сохранении набора полей, объявленных в базовой, см. разд. 16.4.3)
# Под изменением функциональности в таких случаях подразумевается изменение
# состава обрабатываемых моделью записей. Изменить состав обрабатываемых
# моделью записей можно, создав диспетчер который укажет необходимые условия
# фильтрации см. классы SuperRubricManager и SubRubricManager.

# В классе модели SuperRubric укажем в качестве диспетчера записей экземпляр
# SuperRubricManager и не забудем объявить метод __str__, который
# генерирует строковое представление надрубрики - ее название


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = "Надрубрика"
        verbose_name_plural = "Надрубрики"


# Для SubRubric все аналогично
class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return "%s - %s" % (self.super_rubric.name, self.name)

    def name_cnt(self):
        # UNCATEGORIZED
        if self.name == "UNCATEGORIZED":
            return "%s (%d)" % (
                self.name,
                playlist.Playlist.objects.filter(
                    user__username__exact="admin"
                ).count(),
            )
        else:
            return "%s (%d)" % (
                self.name,
                self.playlist_set.filter(
                    user__username__exact="admin"
                ).count(),
            )

    class Meta:
        proxy = True
        ordering = (
            "super_rubric__order",
            "order",
        )
        verbose_name = "Подрубрика"
        verbose_name_plural = "Подрубрики"


# Вся работа с надрубриками и подрубриками будет выполняться
# средствами административного сайта admin.py
