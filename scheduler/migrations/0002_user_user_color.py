# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_color',
            field=models.CharField(default=b'CCCCFF', max_length=6),
            preserve_default=True,
        ),
    ]
