# Generated by Django 2.1.7 on 2019-04-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('competition', '0010_answer_given_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(),
        ),
    ]