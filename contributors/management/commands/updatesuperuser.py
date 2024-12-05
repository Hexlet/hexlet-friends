from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Updates the superuser"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True)
        parser.add_argument("--email", required=True)

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]

        try:
            user = User.objects.get(username=username)
            user.email = email
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} updated successfully")
            )
        except User.DoesNotExist:
            User.objects.create_superuser(username=username, email=email)
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} created successfully")
            )
