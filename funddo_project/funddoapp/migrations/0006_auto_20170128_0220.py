# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funddoapp', '0005_auto_20170126_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='services',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
