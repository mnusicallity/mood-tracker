# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mood', '0007_auto_20160323_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
