# Generated by Django 2.1.7 on 2019-04-28 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0003_auto_20190428_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
