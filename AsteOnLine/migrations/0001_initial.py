# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.contrib.auth.models
from django.utils.timezone import utc
import django.utils.timezone
from django.conf import settings
import django.core.validators
import AsteOnLine.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titolo', models.CharField(max_length=140)),
                ('descrizione', models.TextField(max_length=600)),
                ('foto', models.ImageField(default=b'no_image.png', upload_to=AsteOnLine.models.get_nome)),
                ('data_apertura', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_chiusura', models.DateTimeField(default=datetime.datetime(2015, 7, 8, 10, 36, 50, 701000, tzinfo=utc))),
                ('base_asta', models.DecimalField(default=0.1, max_digits=8, decimal_places=2)),
                ('offerta_corrente', models.DecimalField(default=0.0, max_digits=8, decimal_places=2)),
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
                ('foto', models.ImageField(default=b'no_image.png', upload_to=AsteOnLine.models.get_catName)),
                ('descrizione', models.TextField(max_length=300)),
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
            ],
            options={
                'verbose_name_plural': 'Puntate',
            },
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('indirizzo', models.TextField(default=b'Vuoto', max_length=200)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='puntata',
            name='utente',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
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
