# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funddoapp', '0004_auto_20170126_2015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='recipient',
            new_name='jobseeker',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='services',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
