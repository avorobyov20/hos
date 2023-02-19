from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create admin"

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.create_superuser("admin", email=None, password="secret")
