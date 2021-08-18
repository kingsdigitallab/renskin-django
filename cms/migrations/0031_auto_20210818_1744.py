# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-18 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0030_auto_20210818_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='credit',
            field=models.TextField(blank=True, default='', help_text="The credit line: author, 'full title', year, owner."),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='title',
            field=models.CharField(blank=True, default='', help_text='The complete title of the artwork.', max_length=255),
        ),
    ]
