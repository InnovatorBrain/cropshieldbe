# Generated by Django 5.0.6 on 2024-05-17 04:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurance', '0003_policyapplication_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=100)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('policy_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='insurance.policyapplication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_type', models.CharField(max_length=50)),
                ('card_number', models.CharField(max_length=19)),
                ('card_holder_name', models.CharField(max_length=50)),
                ('expiry_date', models.CharField(max_length=7)),
                ('cvc', models.CharField(max_length=3)),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_methods', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
