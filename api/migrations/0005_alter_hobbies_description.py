# Generated by Django 5.1.1 on 2024-12-10 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_hobbies_description_alter_hobbies_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hobbies",
            name="description",
            field=models.CharField(blank=True, default=None, max_length=254),
        ),
    ]
