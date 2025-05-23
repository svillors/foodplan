# Generated by Django 5.1 on 2025-04-22 20:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Название')),
                ('unit', models.CharField(choices=[('g', 'г'), ('ml', 'мл'), ('pcs', 'шт')], max_length=3)),
                ('price_per_unit', models.FloatField(verbose_name='Цена на еденицу измерения')),
                ('calories_per_unit', models.FloatField(verbose_name='Калории на еденицу измерения')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.IngredientItem', to='recipes.ingredient', verbose_name='Ингредиенты')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientitem',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
