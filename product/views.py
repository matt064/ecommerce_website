from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import Product, Category, Review

def product_detail(request, slug):
    obj = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        rating = request.POST.get('rating', 3)
        content = request.POST.get('content', '')

        if content:
            reviews = Review.objects.filter(created_by=request.user, product=obj)

            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review = Review.objects.create(
                    product = obj,
                    rating = rating,
                    content = content,
                    created_by = request.user
                )

            return redirect('product:detail', slug=slug)

    context = {'obj': obj}
    return render(request, 'product/detail.html', context)