# Generated by Django 2.1.7 on 2019-03-30 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0003_auto_20190330_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='race',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='competition.Competition'),
            preserve_default=False,
        ),
    ]
