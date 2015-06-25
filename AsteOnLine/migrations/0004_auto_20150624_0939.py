# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import AsteOnLine.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0003_auto_20150623_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 1, 7, 39, 58, 998000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asta',
            name='foto',
            field=models.ImageField(default=b'C:\\Users\\Marco\\Esame\\Aste\\static\\media\\nd.gif', upload_to=AsteOnLine.models.get_nome),
        ),
    ]
