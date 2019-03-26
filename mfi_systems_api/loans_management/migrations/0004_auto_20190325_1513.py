# Generated by Django 2.1.7 on 2019-03-25 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loans_management', '0003_auto_20190324_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanDisbursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_disbursed', models.DateTimeField(auto_now_add=True)),
                ('disbursed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disbursal_officer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='loans',
            old_name='loan_disbursed',
            new_name='is_loan_disbursed',
        ),
        migrations.RemoveField(
            model_name='loanapproval',
            name='loan',
        ),
        migrations.AddField(
            model_name='loanapproval',
            name='approved_loan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='loan_approved', to='loans_management.Loans'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='loanapproval',
            name='approved_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approval_officer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='loandisbursal',
            name='disbursed_loan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_disbursed', to='loans_management.Loans'),
        ),
    ]