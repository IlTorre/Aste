# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asta',
            name='offerta_corrente',
            field=models.DecimalField(default=0.01, max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 8, 7, 56, 29, 81000, tzinfo=utc)),
        ),
    ]
