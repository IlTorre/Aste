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
            name='stato',
            field=models.CharField(default=(b'INPREPARAZIONE', b'In preparazione'), max_length=14, choices=[(b'INPREPARAZIONE', b'In preparazione'), (b'SPEDITO', b'Spedito'), (b'RICEVUTO', b'Ricevuto')]),
        ),
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 8, 12, 15, 29, 687000, tzinfo=utc)),
        ),
    ]
