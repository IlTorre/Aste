# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.utils.timezone
from django.conf import settings
import AsteOnLine.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=140)),
                ('descrizione', models.CharField(max_length=600)),
                ('foto', models.ImageField(default=b'nd.gif', upload_to=AsteOnLine.models.get_nome)),
                ('data_apertura', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_chiusura', models.DateTimeField(default=datetime.datetime(2015, 6, 30, 19, 32, 43, 439000, tzinfo=utc))),
                ('base_asta', models.DecimalField(default=0.1, max_digits=8, decimal_places=2)),
            ],
            options={
                'verbose_name_plural': 'Aste',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Categorie',
            },
        ),
        migrations.CreateModel(
            name='Puntata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('importo', models.DecimalField(max_digits=8, decimal_places=2)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('asta', models.ForeignKey(to='AsteOnLine.Asta')),
                ('utente', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Puntate',
            },
        ),
        migrations.AddField(
            model_name='asta',
            name='categoria',
            field=models.ForeignKey(to='AsteOnLine.Categoria'),
        ),
        migrations.AddField(
            model_name='asta',
            name='creatore',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='puntata',
            unique_together=set([('importo', 'asta')]),
        ),
    ]
