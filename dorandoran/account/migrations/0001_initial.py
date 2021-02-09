# Generated by Django 3.1.2 on 2021-02-09 12:54

import account.models
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.PositiveSmallIntegerField(choices=[(1, 'admin'), (2, 'teacher'), (3, 'student')], default=3)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('uid', models.CharField(blank=True, max_length=150, unique=True, verbose_name='user id')),
                ('name', models.CharField(default='unknown', help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, verbose_name='username')),
                ('email', models.EmailField(max_length=128, unique=True, verbose_name='email address')),
            ],
            options={
                'db_table': 'User',
            },
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
    ]
