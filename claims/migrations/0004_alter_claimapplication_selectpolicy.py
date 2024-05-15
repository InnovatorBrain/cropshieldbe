# Generated by Django 5.0.2 on 2024-05-15 08:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0003_alter_claimapplication_selectpolicy'),
        ('insurance', '0003_policyapplication_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claimapplication',
            name='selectPolicy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='claim_applications', to='insurance.policyapplication'),
        ),
    ]