from django.db import models
from django.contrib.auth.models import AbstractUser

"""Стандартная модель пользователя User, предлагаемая стандартным
приложением django.contrib.auth, не подходит, поскольку нам необходимо
хранить дополнительные данные о пользователе. Поэтому создадим
собственную модель, производную от стандартной AbstractUser. Также
нужно сообщить подсистеме разграничения доступа Django о необходимости
использовать нашу модель вместо стандартной (делается это через настройки
AUTH_USER_MODEL = 'main.AdvUser') и прописать ее модуле admin.py"""


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name="Прошел активацию?"
    )

    # переопределим это поле, т.к. нам нужно значение True по умолчанию
    is_staff = models.BooleanField(default=True)

    class Meta(AbstractUser.Meta):
        pass
