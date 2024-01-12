# ruff: noqa: E501
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DeletedRecord",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.JSONField(verbose_name="data")),
                (
                    "table_name",
                    models.CharField(max_length=128, verbose_name="table name"),
                ),
                ("object_id", models.BigIntegerField(verbose_name="object id")),
                ("deleted_at", models.DateTimeField(verbose_name="deleted at")),
            ],
            options={
                "verbose_name": "deleted record",
                "verbose_name_plural": "deleted records",
                "db_table": "django_deletion_record",
                "indexes": [
                    models.Index(
                        fields=["object_id", "table_name"], name="deletion_obj_idx"
                    )
                ],
            },
        ),
        migrations.RunSQL(
            """
            CREATE FUNCTION deletion_record_insert() RETURNS trigger
                LANGUAGE plpgsql
            AS
            $$
            BEGIN
                EXECUTE 'INSERT INTO django_deletion_record (object_id, table_name, data, deleted_at) VALUES ($1, $2, $3, $4)'
                    USING OLD.id, TG_TABLE_NAME, to_jsonb(OLD.*), current_timestamp;
                RETURN OLD;
            END;
            $$;
            """,
            reverse_sql="DROP FUNCTION IF EXISTS deletion_record_insert CASCADE;",
        ),
    ]
