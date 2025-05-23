# Generated by Django 5.2 on 2025-04-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_dailymenu_change_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.CharField(choices=[('menu_type', 'Тип меню'), ('food_intake', 'Приём пищи'), ('allergy', 'Аллергия')], default='food_intake', max_length=20),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='calories_per_unit',
            field=models.FloatField(help_text='калории рассчтываются за 1 кг/литр или же за 1 шт/упаков', verbose_name='Калории на еденицу измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='price_per_unit',
            field=models.FloatField(help_text='цена рассчтывается за 1 кг/литр или же за 1 шт/упаков', verbose_name='Цена на еденицу измерения'),
        ),
    ]
