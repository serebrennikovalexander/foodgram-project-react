# Generated by Django 3.2 on 2023-05-24 17:20

from django.db import migrations

import recipes.utility

INITIAL_INGREDIENTS = recipes.utility.contents


def add_ingredients(apps, schema_editor):
    MainIngredient = apps.get_model('recipes', 'MainIngredient')
    for ingredient in INITIAL_INGREDIENTS:
        new_ingredient = MainIngredient(
            name=ingredient['name'],
            measurement_unit=ingredient['measurement_unit']
        )
        new_ingredient.save()


def remove_ingredients(apps, schema_editor):
    MainIngredient = apps.get_model('recipes', 'MainIngredient')
    for ingredient in INITIAL_INGREDIENTS:
        MainIngredient.objects.get(name=ingredient['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_add_tags'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        ),
    ]
