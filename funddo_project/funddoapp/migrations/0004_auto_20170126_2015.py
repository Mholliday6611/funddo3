# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funddoapp', '0003_userprofile_provider'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='provider',
            new_name='funder',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='recipient',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
