from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:listing_id>/', views.create_booking, name='create_booking'),
    path('detail/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my/', views.my_bookings, name='my_bookings'),
    path('owner/', views.owner_bookings, name='owner_bookings'),
    path('booking-requests/', views.booking_requests_view, name='booking_requests'),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
]
