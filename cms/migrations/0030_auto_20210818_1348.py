# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-18 12:48


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0029_auto_20210817_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitionfeaturepage',
            name='feature_number',
            field=models.IntegerField(blank=True, default=None, help_text='This number should match the one used in the physical exhibition and the map.', null=True),
        ),
    ]
