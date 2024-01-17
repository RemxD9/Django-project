# Generated by Django 4.2.9 on 2024-01-17 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analytics', '0005_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geography',
            name='image',
            field=models.ImageField(null=True, upload_to='staticfiles/geography/graphs', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='geography',
            name='table',
            field=models.FileField(null=True, upload_to='staticfiles/geography/tables', verbose_name='Таблица'),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='image',
            field=models.ImageField(null=True, upload_to='staticfiles/popularity/graphs', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='popularity',
            name='table',
            field=models.FileField(null=True, upload_to='staticfiles/popularity/tables', verbose_name='Таблица'),
        ),
        migrations.AlterField(
            model_name='skills',
            name='image',
            field=models.ImageField(null=True, upload_to='staticfiles/skills/graphs', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='skills',
            name='table',
            field=models.FileField(null=True, upload_to='staticfiles/skills/tables', verbose_name='Таблица'),
        ),
    ]
