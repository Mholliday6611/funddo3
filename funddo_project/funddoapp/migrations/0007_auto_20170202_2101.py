# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funddoapp', '0006_auto_20170128_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='funded',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='request',
            name='email',
            field=models.EmailField(max_length=255),
            preserve_default=True,
        ),
    ]
