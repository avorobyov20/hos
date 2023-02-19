from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.mixins import UserPassesTestMixin


class HosPasswordResetCompleteView(
    UserPassesTestMixin, PasswordResetCompleteView
):
    template_name = "main/password_complete.html"

    def test_func(self):
        return not self.request.user.is_authenticated
