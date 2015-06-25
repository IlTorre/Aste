# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import AsteOnLine.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AsteOnLine', '0005_auto_20150624_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asta',
            name='data_chiusura',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 1, 8, 51, 6, 626000, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='asta',
            name='foto',
            field=models.ImageField(default=b'no_image.jpg', upload_to=AsteOnLine.models.get_nome),
        ),
    ]
