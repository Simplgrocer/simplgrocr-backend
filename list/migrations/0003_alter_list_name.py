# Generated by Django 5.0.3 on 2024-03-11 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("list", "0002_rename_shoppinglist_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
