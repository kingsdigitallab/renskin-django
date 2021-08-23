# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-19 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0031_auto_20210818_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='credit',
            field=models.TextField(blank=True, default='', help_text='e.g. Chistoph Weiditz, TITLE, 1529, Germanisches National Museum. TITLE will be substituted by the title field.', verbose_name='Credit line'),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='title',
            field=models.CharField(blank=True, default='', help_text='The complete title of the artwork. Without author name, date or any other information.', max_length=255),
        ),
    ]