# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-13 17:17


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0027_auto_20210812_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='title',
            field=models.CharField(blank=True, default='', help_text='To use the image title, leave this field empty.', max_length=255),
        ),
    ]
