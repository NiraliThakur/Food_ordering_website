# Generated by Django 5.0.1 on 2024-06-13 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Food_ordering_app', '0005_menuitem_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='toppings',
            field=models.ManyToManyField(blank=True, to='Food_ordering_app.pizzatopping'),
        ),
        migrations.AddField(
            model_name='pizzatopping',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
