# Generated by Django 3.0.7 on 2020-06-17 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200617_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='membership',
            field=models.SmallIntegerField(choices=[(0, 'VIP'), (1, 'NORMAL')], null=True),
        ),
    ]
