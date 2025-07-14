from django.urls import path
from . import views

urlpatterns = [
    path('listings/', views.ListingView.as_view(), name='listings'),
    path('listings/<int:pk>/', views.ListingView.as_view(),
         name='listing_detail'),
    path('listings/create/', views.create_listing, name='create_listing'),
    path('my-listings/', views.UserListingsView.as_view(),
         name='user_listings'),
]
