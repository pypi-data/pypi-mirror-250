# ruff: noqa: E501
import textwrap

from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = _(
        "Get migration operations to register models for deletion records. To"
        " apply these operations, you need to create an empty migration file"
        " for the related app and insert generated operations."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "models",
            nargs="+",
            help=_(
                "Space seperated list of models in the format of `appname.ModelName`"
            ),
        )

    def get_operation(self, name: str, table_name: str) -> str:
        code = textwrap.dedent(
            """
            operations = [
                migrations.RunSQL(
                    \"\"\"
                    CREATE TRIGGER deleted_record_insert
                        AFTER DELETE
                        ON %(table_name)s
                        FOR EACH ROW
                    EXECUTE FUNCTION deletion_record_insert();
                    \"\"\",
                    reverse_sql="DROP TRIGGER IF EXISTS deleted_record_insert ON %(table_name)s CASCADE;",
                )
            ]\n
            """
        )
        code = code % {"table_name": table_name}
        header = f"# {name}"
        return header + code

    def handle(self, *args, **options):
        models = dict.fromkeys(options["models"])
        for name in models:
            model = apps.get_model(name)
            table = model._meta.db_table
            self.stdout.write(self.get_operation(name, table))

        if models:
            deps = textwrap.dedent(
                """
                # Add this only if it is not added in previous migrations.
                dependencies = [
                    ("deletion_records", "0001_initial"),
                ]
                """
            )
            self.stdout.write(deps)
