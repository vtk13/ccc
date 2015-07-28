# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20150726_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('image', models.ImageField(upload_to='')),
                ('good', models.ForeignKey(to='goods.Good')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='good',
            name='parent',
            field=models.ForeignKey(to='goods.Good', null=True, blank=True),
            preserve_default=True,
        ),
    ]
