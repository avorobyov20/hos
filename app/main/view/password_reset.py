from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class HosPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = "main/password_reset.html"
    subject_template_name = "email/reset_letter_subject.txt"
    email_template_name = "email/reset_letter_body.txt"
    success_url = reverse_lazy("main:password_reset_done")

    def test_func(self):
        return not self.request.user.is_authenticated
