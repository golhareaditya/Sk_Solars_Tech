import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a Django admin user from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping admin user setup because DJANGO_SUPERUSER_USERNAME "
                    "or DJANGO_SUPERUSER_PASSWORD is not set."
                )
            )
            return

        User = get_user_model()
        defaults = {
            "email": email or "",
            "is_staff": True,
            "is_superuser": True,
            "is_active": True,
        }

        user, created = User.objects.get_or_create(username=username, defaults=defaults)

        updated_fields = []
        for field, value in defaults.items():
            if getattr(user, field, None) != value:
                setattr(user, field, value)
                updated_fields.append(field)

        if not user.check_password(password):
            user.set_password(password)
            updated_fields.append("password")

        if created or updated_fields:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created admin user '{username}'"))
            return

        if updated_fields:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Updated admin user '{username}' ({', '.join(updated_fields)})"
                )
            )
            return

        self.stdout.write(self.style.SUCCESS(f"Admin user '{username}' already exists"))
