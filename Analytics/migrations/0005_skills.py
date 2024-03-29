# Generated by Django 4.2.9 on 2024-01-17 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analytics', '0004_alter_geography_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('image', models.ImageField(null=True, upload_to='staticfiles', verbose_name='Изображение')),
                ('table', models.FileField(null=True, upload_to='', verbose_name='Таблица')),
            ],
            options={
                'verbose_name': 'Навыки',
                'verbose_name_plural': 'Навыки',
                'db_table': 'Skills',
            },
        ),
    ]
