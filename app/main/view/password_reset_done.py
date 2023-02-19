from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.mixins import UserPassesTestMixin


class HosPasswordResetDoneView(UserPassesTestMixin, PasswordResetDoneView):
    template_name = "main/password_reset_done.html"

    def test_func(self):
        return not self.request.user.is_authenticated
