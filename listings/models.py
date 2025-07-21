from django.db import models
from accounts.models import CustomUser as User

# Create your models here.


class Listing(models.Model):
    """
    Model representing a listing for a product or service.
    """
    CATEGORY_CHOICES = [
        ('tool', 'Tool'),
        ('book', 'Book'),
        ('parking', 'Parking Spot'),
        ('other', 'Other'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,
                                default='other')
    location = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
