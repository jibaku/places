# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 15:35
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_picture-and-links'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='country',
            field=models.CharField(blank=True, max_length=100, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='place',
            name='place_attributes',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='placelink',
            name='link_type',
            field=models.CharField(choices=[('website', 'Website'), ('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('pinterest', 'Pinterest')], default='website', max_length=20),
        ),
    ]