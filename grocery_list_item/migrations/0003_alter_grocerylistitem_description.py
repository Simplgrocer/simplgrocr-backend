# Generated by Django 4.2.11 on 2024-04-15 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery_list_item', '0002_remove_grocerylistitem_per_measurement_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grocerylistitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]