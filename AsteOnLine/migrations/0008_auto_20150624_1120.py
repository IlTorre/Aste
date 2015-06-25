# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0007_auto_20150624_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 1, 9, 20, 9, 578000, tzinfo=utc)),
        ),
    ]
