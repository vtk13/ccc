# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=10)),
                ('discount', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('bar_code', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('packed', models.BooleanField(default=False)),
                ('pack_volume', models.DecimalField(decimal_places=3, max_digits=10)),
                ('parent', models.ForeignKey(to='goods.Good')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='good',
            name='unit',
            field=models.ForeignKey(to='goods.Unit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cost',
            name='good',
            field=models.ForeignKey(to='goods.Good'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cost',
            name='shop',
            field=models.ForeignKey(to='goods.Shop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cost',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
