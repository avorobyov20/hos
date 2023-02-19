from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create user"

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.create_user(
            "user", email=None, password="password", is_staff=True
        )
