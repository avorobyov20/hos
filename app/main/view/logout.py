from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.safestring import mark_safe


class HosLogoutView(LoginRequiredMixin, LogoutView):
    """Примесь LoginRequiredMixin запрещает доступ к контроллеру гостям.
    Вместо запрашиваемой страницы будет выведена та, что указана
    в LOGOUT_REDIRECT_URL, если такой параметр задан.
    У нас этот параметр равен / и лучше оставить его таким"""

    template_name = "main/logout.html"

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.SUCCESS,
            mark_safe(
                "До свидания, <b>"
                + request.user.username
                + "</b><p>Вы вышли из учетной записи.</p>"
            ),
        )
        response = super().dispatch(request, *args, **kwargs)
        return response
