# Generated by Django 3.0.5 on 2020-04-04 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zettelbox', '0005_remove_paper_inside'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='creator',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='creator_id', to='zettelbox.User'),
            preserve_default=False,
        ),
    ]
