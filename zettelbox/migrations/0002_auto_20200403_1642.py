# Generated by Django 3.0.5 on 2020-04-03 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zettelbox', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='box',
            name='full',
        ),
        migrations.RemoveField(
            model_name='box',
            name='holder',
        ),
        migrations.AlterField(
            model_name='box',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='box',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
