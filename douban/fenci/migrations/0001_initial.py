# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('com_name', models.CharField(max_length=20)),
                ('com_star', models.CharField(max_length=10)),
                ('short', models.CharField(max_length=350)),
                ('comment_vote', models.IntegerField(default=0)),
                ('movie_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MovieName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=20)),
            ],
        ),
    ]
