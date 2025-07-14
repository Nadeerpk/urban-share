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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_listing(request):
    form = ListingForm()
    return render(request, 'listings/create_listing.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ListingView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        if pk:
            listing = Listing.objects.get(pk=pk)
            return render(request, 'listings/listing_detail.html',
                          {'listing': listing})
        listings = Listing.objects.all()
        return render(request, 'listings/all_listings.html',
                      {'listings': listings})

    def post(self, request):
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # Set the owner here
            listing.save()
            return redirect('listings')
        return render(request, 'listings/create_listing.html', {'form': form})

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
