# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import AsteOnLine.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0004_auto_20150624_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 1, 8, 7, 23, 380000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asta',
            name='foto',
            field=models.ImageField(default=b'C:\\Users\\Marco\\Esame\\Aste\\media\\no_image.jpg', upload_to=AsteOnLine.models.get_nome),
        ),
    ]
