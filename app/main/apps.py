from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import send_activation_notification


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main"
    verbose_name = "hearts of space"


"""Для отправки письма о необходимости активации объявим свой сигнал.
Называться он будет user_registered и получит в качестве единственного
параметра instance объект только что созданного пользователя.
Модуль apps.py, который выполняется непосредственно при инициализации
приложения, является идеальным местом для записи кода, объявляющего
сигналы и привязывающего к ним обработчики."""
user_registered = Signal()


def user_registered_dispatcher(sender, **kwargs):
    """функция, отвечающая за отправку письма-оповещения об активации"""
    send_activation_notification(kwargs["instance"])


# привязываем к сигналу обработчик
user_registered.connect(user_registered_dispatcher)
