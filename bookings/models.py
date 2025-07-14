from django.db import models

# Create your models here.


class Booking(models.Model):
    """
    Model representing a booking for a listing.
    """
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.listing.title} from {self.start_date} to {self.end_date}"