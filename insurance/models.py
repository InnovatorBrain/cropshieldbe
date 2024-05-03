from django.db import models


class PolicyApplication(models.Model):
    # Personal Information
    farmerName = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    dateOfBirth = models.CharField(max_length=15, null=True, blank=True)

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("agender", "Agender"),
        ("androgyne", "Androgyne"),
        ("bigender", "Bigender"),
        ("genderfluid", "Genderfluid"),
        ("genderqueer", "Genderqueer"),
        ("nonbinary", "Non-binary"),
        ("prefer_not_to_say", "Prefer not to say"),
    ]

    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, null=True, blank=True
    )
    cnic = models.CharField(max_length=13, null=True, blank=True)
    countryCode = models.CharField(max_length=4, null=True, blank=True)
    phoneNumber = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    passportPicture1 = models.ImageField(upload_to="passport/", null=True, blank=True)
    cnicPicture1 = models.ImageField(upload_to="cnic/", null=True, blank=True)
    cnicPicture2 = models.ImageField(upload_to="cnic/", null=True, blank=True)
    domicilePicture = models.ImageField(upload_to="domicile/", null=True, blank=True)

    # Farm Information
    farmAddress = models.TextField(null=True, blank=True)

    CROP_CHOICES = [
        ("Wheat", "Wheat"),
        ("Rice", "Rice"),
        ("Cotton", "Cotton"),
        ("Sugarcane", "Sugarcane"),
        ("Other", "Other"),
    ]
    cropsInsured = models.CharField(
        max_length=255, choices=CROP_CHOICES, null=True, blank=True
    )
    otherCrop = models.CharField(max_length=255, null=True, blank=True)
    acreagePlanted = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    cropVariety = models.CharField(max_length=255, null=True, blank=True)
    plantingDate = models.CharField(max_length=15, null=True, blank=True)

    # Insurance Details
    POLICY_CHOICES = [
        ("policy1", "Ins Crop"),
        ("policy2", "New ven"),
        ("policy3", "Smart Policy"),
    ]
    selectPolicy = models.CharField(
        max_length=255, choices=POLICY_CHOICES, null=True, blank=True
    )
    coverageAmount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    startDate = models.CharField(max_length=15, null=True, blank=True)
    endDate = models.CharField(max_length=15, null=True, blank=True)

    RISK_FACTOR_CHOICES = [
        ("Floods", "Floods"),
        ("Droughts", "Droughts"),
        ("Hailstorms", "Hailstorms"),
        ("CommonPest1", "Pest and Disease Risks"),
    ]
    riskFactor = models.CharField(
        max_length=255, choices=RISK_FACTOR_CHOICES, null=True, blank=True
    )
    additionalComments = models.TextField(null=True, blank=True)

    # Payment
    PAYMENT_METHOD_CHOICES = [
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
    ]
    paymentMethod = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True
    )
    cardNumber = models.CharField(max_length=19, null=True, blank=True)
    cardHolderName = models.CharField(max_length=50, null=True, blank=True)
    expiryDate = models.CharField(max_length=7, null=True, blank=True)
    cvc = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.farmerName

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("DENIED", "Denied"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
