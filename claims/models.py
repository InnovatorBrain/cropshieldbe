from django.db import models


class ClaimApplication(models.Model):
    # Claim Application
    TYPE_OF_DAMAGE_CHOICES = [
        ('weather_related', 'Weather-related'),
        ('pest_related', 'Pest-related'),
        ('disease_related', 'Disease-related'),
        ('mechanical_damage', 'Mechanical damage')
    ]
    
    createdAt = models.DateTimeField(auto_now_add=True)
    typeOfDamage = models.CharField(max_length=20, choices=TYPE_OF_DAMAGE_CHOICES)
    dateOfDamage = models.CharField(max_length=20)
    EXTENT_OF_DAMAGE_CHOICES = [
        ('0-25%', '0-25% Crop Loss'),
        ('26-50%', '26-50% Crop Loss'),
        ('51-75%', '51-75% Crop Loss'),
        ('76-100%', '76-100% Crop Loss')
    ]
    extentOfDamage = models.CharField(max_length=10, choices=EXTENT_OF_DAMAGE_CHOICES)
    witnessName = models.CharField(max_length=50)
    witnessCNIC = models.CharField(max_length=13)
    COUNTRY_CODE_CHOICES = [
        ('+1', '+1 (USA)'),
        ('+44', '+44 (UK)'),
        ('+92', '+92 (Pakistan)'),
        ('+970', '+970 (Palestine)'),
        ('+20', '+20 (Egypt)'),
        ('+962', '+962 (Jordan)'),
        ('+971', '+971 (UAE)')
    ]

    countryCode = models.CharField(max_length=5, choices=COUNTRY_CODE_CHOICES)
    witnessPhoneNumber = models.CharField(max_length=20)
    damageDescription = models.CharField(max_length=500)

    # Contact Details
    farmerName = models.CharField(max_length=50, null=True, blank=True)
    COUNTRY_CODE_CHOICES = [
        ('+1', '+1 (USA)'),
        ('+44', '+44 (UK)'),
        ('+92', '+92 (Pakistan)'),
        ('+970', '+970 (Palestine)'),
        ('+20', '+20 (Egypt)'),
        ('+962', '+962 (Jordan)'),
        ('+971', '+971 (UAE)')
    ]

    countryCode = models.CharField(max_length=5, choices=COUNTRY_CODE_CHOICES)
    phoneNumber = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    
    # Document section
    claimPicture1 = models.ImageField(upload_to='claim_pictures/', null=True, blank=True)
    claimPicture2 = models.ImageField(upload_to='claim_pictures/', null=True, blank=True)
    claimPicture3 = models.ImageField(upload_to='claim_pictures/', null=True, blank=True)
    claimPicture4 = models.ImageField(upload_to='claim_pictures/', null=True, blank=True)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

