# Generated by Django 4.2.11 on 2024-04-09 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grocery_list', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroceryListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('rate_measurement_quantity', models.FloatField()),
                ('rate_measurement_unit', models.CharField(choices=[('Unit', 'Unit'), ('Kilogram', 'Kilogram'), ('Gram', 'Gram')], max_length=8)),
                ('rate', models.FloatField()),
                ('quantity_measurement_unit', models.CharField(choices=[('Unit', 'Unit'), ('Kilogram', 'Kilogram'), ('Gram', 'Gram')], max_length=8)),
                ('per_measurement_unit_price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('grocery_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grocery_list.grocerylist')),
            ],
        ),
    ]
