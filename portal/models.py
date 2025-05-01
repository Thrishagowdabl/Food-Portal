from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    USER_TYPE_CHOICES = [("donor", "Donor"), ("receiver", "Receiver")]
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="donor"
    )

    def __str__(self):
        return self.username


# Donor profile model
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Donor: {self.user.username}"


# Receiver profile model
class Receiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Receiver: {self.user.username}"


# Donation model
class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    food_type = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    pickup_location = models.CharField(max_length=255)
    pickup_time = models.DateTimeField()
    expiry_date = models.DateField()
    status = models.CharField(default="Available", max_length=20)

    def __str__(self):
        return f"{self.food_type} by {self.donor.username}"


# Request model
class Request(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.requester.username} on {self.donation.food_type}"
