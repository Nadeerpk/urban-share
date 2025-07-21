from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm

# Create your views here.

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return redirect('listing_detail', pk=review.listing.pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', pk=review.listing.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user == request.user and request.method == 'POST':
        listing_pk = review.listing.pk
        review.delete()
        return redirect('listing_detail', pk=listing_pk)
    return redirect('listing_detail', pk=review.listing.pk)
