# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0017_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(default='asd', max_length=50),
            preserve_default=False,
        ),
    ]
