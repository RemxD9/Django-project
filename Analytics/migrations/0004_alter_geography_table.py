# Generated by Django 4.2.9 on 2024-01-17 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Analytics', '0003_alter_geography_image_alter_popularity_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geography',
            name='table',
            field=models.FileField(null=True, upload_to='', verbose_name='Таблица'),
        ),
    ]
