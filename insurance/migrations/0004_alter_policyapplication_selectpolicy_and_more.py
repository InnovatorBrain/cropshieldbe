# Generated by Django 5.0.6 on 2024-05-18 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0003_policyapplication_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyapplication',
            name='selectPolicy',
            field=models.CharField(blank=True, choices=[('HarvestGuard_Assurance', 'HarvestGuard Assurance'), ('CropShield_Secure', 'CropShield Secure'), ('AgriGuard_Plus', 'AgriGuard Plus'), ('FarmShield_Complete', 'FarmShield Complete'), ('CropSafe_Prime', 'CropSafe Prime')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='policypremiumdeductible',
            name='selectPolicy',
            field=models.CharField(choices=[('HarvestGuard_Assurance', 'HarvestGuard Assurance'), ('CropShield_Secure', 'CropShield Secure'), ('AgriGuard_Plus', 'AgriGuard Plus'), ('FarmShield_Complete', 'FarmShield Complete'), ('CropSafe_Prime', 'CropSafe Prime')], max_length=255, unique=True),
        ),
    ]
