from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class HosPasswordResetConfirmView(
    UserPassesTestMixin, PasswordResetConfirmView
):
    template_name = "main/password_confirm.html"
    success_url = reverse_lazy("main:password_reset_complete")

    def test_func(self):
        return not self.request.user.is_authenticated
