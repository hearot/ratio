# Generated by Django 2.1.7 on 2019-03-30 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='contestants',
            field=models.ManyToManyField(default=[], to='competition.Contestant'),
        ),
        migrations.AlterField(
            model_name='contestant',
            name='answers',
            field=models.ManyToManyField(default=[], to='competition.Answer'),
        ),
    ]
