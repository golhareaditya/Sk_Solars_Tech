import os
import tempfile

import dj_database_url
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = "Migrate data from the current default database into a PostgreSQL database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--database-url",
            help="Target PostgreSQL database URL. If omitted, uses DATABASE_URL env var.",
        )
        parser.add_argument(
            "--data-file",
            help="Path to temporary data dump file. Default is a temp JSON file.",
        )
        parser.add_argument(
            "--exclude",
            action="append",
            default=["auth.permission", "contenttypes"],
            help="App.Model to exclude from dump. Can be repeated.",
        )

    def handle(self, *args, **options):
        database_url = options.get("database_url") or os.environ.get("DATABASE_URL")
        if not database_url:
            raise CommandError(
                "Provide a PostgreSQL URL with --database-url or set DATABASE_URL in the environment."
            )

        normalized_url = database_url.strip()
        if normalized_url.startswith("sqlite"):
            raise CommandError("Target database URL must point to PostgreSQL, not SQLite.")

        exclude = options.get("exclude") or []
        data_file = options.get("data_file")
        temp_file_created = False

        if not data_file:
            temp_handle = tempfile.NamedTemporaryFile(
                suffix=".json",
                delete=False,
                mode="w",
                encoding="utf-8",
            )
            data_file = temp_handle.name
            temp_handle.close()
            temp_file_created = True

        self.stdout.write(self.style.NOTICE("Dumping current default database..."))
        with open(data_file, "w", encoding="utf-8") as dump_file:
            call_command("dumpdata", *exclude, stdout=dump_file, format="json")

        self.stdout.write(self.style.NOTICE(f"Dump saved to {data_file}"))

        self.stdout.write(self.style.NOTICE("Configuring target PostgreSQL database..."))
        settings.DATABASES["postgres_migrate_target"] = dj_database_url.parse(
            normalized_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not settings.DEBUG,
        )
        connections.close_all()

        self.stdout.write(self.style.NOTICE("Applying migrations to PostgreSQL target..."))
        call_command("migrate", database="postgres_migrate_target", interactive=False)

        self.stdout.write(self.style.NOTICE("Loading dumped data into PostgreSQL..."))
        call_command("loaddata", data_file, database="postgres_migrate_target")

        if temp_file_created:
            try:
                os.remove(data_file)
            except OSError:
                self.stdout.write(
                    self.style.WARNING(
                        f"Could not delete temporary dump file {data_file}."
                    )
                )

        self.stdout.write(self.style.SUCCESS("SQLite to PostgreSQL migration complete."))
