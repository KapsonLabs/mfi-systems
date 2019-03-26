# Generated by Django 2.1.7 on 2019-03-25 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loans_management', '0005_auto_20190325_1658'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('fined_amount', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True)),
                ('comment', models.TextField()),
                ('date_paid', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_confirmation_officer', to=settings.AUTH_USER_MODEL)),
                ('related_loan_cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans_management.LoanCycles')),
            ],
        ),
    ]