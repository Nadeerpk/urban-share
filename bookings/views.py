from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from listings.models import Listing
from bookings.tasks import send_email_notification


@login_required
def create_booking(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if listing.owner == request.user:
        messages.error(request, "You can't book your own resource.")
        return redirect('listing_detail', pk=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            overlapping = Booking.objects.filter(listing=listing,
                                                 start_date__lte=form.cleaned_data['end_date'],
                                                 end_date__gte=form.cleaned_data['start_date'],
                                                 status='approved').exists()

            if overlapping:
                messages.error(request, "This resource is already booked during that period.")
                return redirect('listing_detail', pk=listing_id)
            booking = form.save(commit=False)
            booking.user = request.user
            booking.listing = listing
            booking.save()
            send_email_notification.delay(
                "New Booking",
                f"You have a new booking request for {listing.title}",
                [listing.owner.email])
            messages.success(request, "Booking request sent successfully.")
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form, 'listing': listing})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def owner_bookings(request):
    listings = Listing.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(listing__in=listings).order_by('-created_at')
    return render(request, 'bookings/owner_bookings.html', {'bookings': bookings})


@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.listing.owner == request.user and booking.status == 'pending' and request.method == 'POST':
        booking.status = 'approved'
        booking.save()
        # Send email notification to the user
        send_email_notification.delay(
            'Booking Approved',
            f'Your booking for {booking.listing.title} has been approved.',
            [booking.user.email]
        )
    return redirect('owner_bookings')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.listing.owner == request.user and booking.status == 'pending' and request.method == 'POST':
        booking.status = 'rejected'
        booking.save()
        send_email_notification.delay(
            'Booking Rejected',
            f'Your booking for {booking.listing.title} has been rejected.',
            [booking.user.email]
        )
    return redirect('owner_bookings')
