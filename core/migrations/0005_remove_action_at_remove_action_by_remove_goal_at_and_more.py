# Generated by Django 4.1.2 on 2022-11-28 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_rename_created_at_action_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="action",
            name="at",
        ),
        migrations.RemoveField(
            model_name="action",
            name="by",
        ),
        migrations.RemoveField(
            model_name="goal",
            name="at",
        ),
        migrations.RemoveField(
            model_name="goal",
            name="by",
        ),
        migrations.AddField(
            model_name="action",
            name="archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="action",
            name="complete",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="goal",
            name="complete",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="goal",
            name="archived",
            field=models.BooleanField(default=False),
        ),
    ]
