# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import AsteOnLine.models


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0002_auto_20150701_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 7, 7, 44, 7, 789000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asta',
            name='foto',
            field=models.ImageField(default=b'no_image.png', upload_to=AsteOnLine.models.get_nome),
        ),
        migrations.AlterField(
            model_name='asta',
            name='offerta_corrente',
            field=models.DecimalField(default=0.0, max_digits=8, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='foto',
            field=models.ImageField(default=b'no_image.png', upload_to=AsteOnLine.models.get_catName),
        ),
    ]
