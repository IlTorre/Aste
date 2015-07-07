# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0002_auto_20150707_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 8, 13, 20, 0, 878000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asta',
            name='stato',
            field=models.CharField(default=(b'In preparazione', b'In preparazione'), max_length=15, choices=[(b'In preparazione', b'In preparazione'), (b'Spedito', b'Spedito'), (b'Ricevuto', b'Ricevuto')]),
        ),
    ]
