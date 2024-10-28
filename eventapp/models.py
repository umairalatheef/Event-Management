from django.db import models
from django.utils import timezone
from django.conf import settings
import os

# Booking Model
class Booking(models.Model):
    event_name = models.CharField(max_length=255, default='Default Event')
    event_place = models.CharField(max_length=255, default='Default Place')
    email = models.EmailField(default='example@example.com')
    event_date = models.DateField()
    mobile_number = models.CharField(max_length=15, default='')
    number_of_persons = models.PositiveIntegerField(default=1)
    description = models.TextField(default='Default description')
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        self.number_of_persons *= 250  # Automatic multiplication with 250
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event_name} at {self.event_place} on {self.event_date}"

# Event Model
def get_default_image():
    # Ensure you have an image in your media folder named 'default_event_image.jpg'
    return os.path.join(settings.MEDIA_URL, 'default_images/default_event_image.jpg')

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', default=get_default_image)

    def __str__(self):
        return self.event_name

#review model
class Review(models.Model):
    SATISFACTION_CHOICES = [
        ('poor', 'Poor'),
        ('average', 'Average'),
        ('good', 'Good'),
        ('very_good', 'Very Good'),
        ('excellent', 'Excellent'),
    ]

    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    satisfaction_level = models.CharField(
        max_length=20, 
        choices=SATISFACTION_CHOICES, 
        default='average'  # Set the default value here
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review for Booking {self.booking.id}"

    
 

