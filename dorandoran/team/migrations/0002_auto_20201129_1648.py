# Generated by Django 3.1.2 on 2020-11-29 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='linkedteamuser',
            table='LinkedTeamUser',
        ),
        migrations.AlterModelTable(
            name='team',
            table='Team',
        ),
    ]