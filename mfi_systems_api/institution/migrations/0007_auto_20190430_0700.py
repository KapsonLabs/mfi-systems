# Generated by Django 2.1.7 on 2019-04-30 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0006_remove_institutionstaff_staff_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionstaff',
            name='phone_dialing_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='institutionstaff',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='institutionstaff',
            name='staff_responsibility',
            field=models.TextField(blank=True, null=True),
        ),
    ]
