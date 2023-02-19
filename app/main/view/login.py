from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.safestring import mark_safe

"""Для реализации входа создадим подкласс контроллера класса LoginView,
в котором опишем все необходимые для работы контроллера параметры.
На самом деле нам понадобится указать только путь к файлу шаблона."""


class HosLoginView(LoginView):
    template_name = "main/login.html"

    # Остальные параметры сохранят значения по умолчанию
    # так как мы собираемся следовать принятым в Django соглашениям

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        # в данном случае add_message вызывается после super().dispatch

        if request.user.is_authenticated:
            messages.add_message(
                request,
                messages.SUCCESS,
                mark_safe(
                    "Здравствуйте, <b>"
                    + request.user.username
                    + "</b><p>Вы вошли в учетную запись.</p>"
                ),
            )
        return response
