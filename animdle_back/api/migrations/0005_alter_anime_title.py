# Generated by Django 4.2.4 on 2023-08-29 08:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_alter_theme_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anime",
            name="title",
            field=models.CharField(max_length=200),
        ),
    ]
