# Generated by Django 2.1.7 on 2019-04-04 16:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('competition', '0008_auto_20190402_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='can_join_when_started',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='delta',
            field=models.IntegerField(default=-5, validators=[django.core.validators.MaxValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='question',
            name='minimum',
            field=models.IntegerField(default=65, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='question',
            name='wrong',
            field=models.IntegerField(default=-10, validators=[django.core.validators.MaxValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='question',
            name='point',
            field=models.IntegerField(default=100, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
