from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin


class RegisterDoneView(UserPassesTestMixin, TemplateView):
    """32.15 Контроллер, который выведет сообщение об успешной регистрации,
    будет называться RegisterDoneView и, в силу его исключительной простоты,
    станет производным от класса TemplateView"""

    template_name = "main/register_done.html"

    def test_func(self):
        return not self.request.user.is_authenticated
