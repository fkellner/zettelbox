# Generated by Django 3.0.5 on 2020-04-04 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zettelbox', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='holder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='zettelbox.User'),
        ),
    ]