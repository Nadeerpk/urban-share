from django.shortcuts import render, redirect
from .models import Listing
from .forms import ListingForm
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from django.views import View  # Add this import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()

    return render(request, 'listings/create_listing.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ListingView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk=None):
        if pk:
            from reviews.models import Review
            from reviews.forms import ReviewForm
            from django.db.models import Avg
            from django.shortcuts import get_object_or_404
            try:
                listing = get_object_or_404(Listing, pk=pk)
                reviews = Review.objects.filter(listing=listing).order_by('-created_at')
                average_rating = reviews.aggregate(avg=Avg('rating'))['avg']
                review_form = ReviewForm()
                return render(request, 'listings/listing_detail.html',
                              {'listing': listing, 'reviews': reviews, 'review_form': review_form, 'average_rating': average_rating})
            except (ValueError, TypeError):
                # Handle invalid pk format
                from django.http import Http404
                raise Http404("Invalid listing ID")
        listings = Listing.objects.all()
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        location = request.GET.get('location', '')
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
        return render(request, 'accounts/home.html',
                      context)

    def post(self, request, pk=None):
        if pk:
            from reviews.models import Review
            from reviews.forms import ReviewForm
            from django.db.models import Avg
            listing = Listing.objects.get(pk=pk)
            reviews = Review.objects.filter(listing=listing).order_by('-created_at')
            average_rating = reviews.aggregate(avg=Avg('rating'))['avg']
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.listing = listing
                review.save()
                return redirect('listing_detail', pk=listing.pk)
            return render(request, 'listings/listing_detail.html',
                          {'listing': listing, 'reviews': reviews, 'review_form': review_form, 'average_rating': average_rating})
        # fallback to original post for create listing
        return super().post(request)

    def patch(self, request, pk):
        listing = Listing.objects.get(pk=pk)
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings')
        return render(request, 'listings/edit_listing.html',
                      {'form': form, 'listing': listing})

    def delete(self, request, pk):
        listing = Listing.objects.get(pk=pk)
        listing.delete()
        return redirect('listings')


@method_decorator(login_required, name='dispatch')
class UserListingsView(View):
    def get(self, request):
        listings = Listing.objects.filter(owner=request.user)
        return render(request, 'listings/user_listings.html',
                      {'listings': listings})
