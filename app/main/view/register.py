from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from main.models import AdvUser
from main.forms.registeruser import RegisterUserForm
from django.contrib.auth.mixins import UserPassesTestMixin


class RegisterUserView(UserPassesTestMixin, CreateView):
    """32.4.1 Контроллер-класс, регистрирующий пользователя
    сделаем производным от CreateView"""

    model = AdvUser
    template_name = "main/register_user.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("main:register_done")

    def test_func(self):
        return not self.request.user.is_authenticated
