# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 11:49


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_event_eventindexpage_eventtag_pasteventindexpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time_end',
            field=models.TimeField(blank=True, null=True, verbose_name='End Time (leave blank if not required)'),
        ),
    ]
