# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funddoapp', '0002_auto_20170126_0534'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='provider',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
