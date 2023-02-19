from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.safestring import mark_safe


class HosPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """32.3.2 Веб-страница правки пароля
    Контроллер-класс HosPasswordChangeView, выводящий эту страницу,
    сделаем производным от стандартного PasswordChangeView"""

    template_name = "main/password_change.html"
    success_url = reverse_lazy("main:index")

    def setup(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.add_message(
                request,
                messages.SUCCESS,
                mark_safe(
                    "Уважаемый пользователь <b>"
                    + request.user.username
                    + "</b><p>Ваш пароль был изменен.</p>"
                ),
            )
        return super().setup(request, *args, **kwargs)
