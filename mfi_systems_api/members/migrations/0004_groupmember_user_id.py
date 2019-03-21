# Generated by Django 2.1.7 on 2019-03-20 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0003_remove_groupmember_member_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='user_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='member_related_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
