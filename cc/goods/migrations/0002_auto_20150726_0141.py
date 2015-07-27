# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='parent',
            field=models.ForeignKey(null=True, to='goods.Good'),
            preserve_default=True,
        ),
    ]
