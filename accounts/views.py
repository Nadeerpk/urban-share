from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser
from listings.models import Listing


def home(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    listings = Listing.objects.all()
    if query:
        listings = listings.filter(title__icontains=query)
    if category:
        listings = listings.filter(category=category)
    if location:
        listings = listings.filter(location__icontains=location)
    categories = Listing.CATEGORY_CHOICES
    context = {
        'listings': listings,
        'query': query,
        'category': category,
        'location': location,
        'categories': categories
    }
    if request.user.is_authenticated:
        from bookings.models import Booking
        from messaging.models import MessageThread
        user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
        owner_listings = Listing.objects.filter(owner=request.user)
        owner_bookings = Booking.objects.filter(listing__in=owner_listings).order_by('-created_at')
        chat_threads = MessageThread.objects.filter(participants=request.user).order_by('-created_at')
        context['user_bookings'] = user_bookings
        context['owner_bookings'] = owner_bookings
        context['chat_threads'] = chat_threads
    return render(request, 'accounts/home.html', context)


# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = CustomUser.objects.create_user(username=username,
                                                  email=email,
                                                  password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/signup.html')


def login_view(request):
    print(request.POST)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'accounts/logout.html')


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response
