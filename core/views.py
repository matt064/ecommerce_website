from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from product.models import Product, Category
from .forms import SingUpForm

def frontpage(request):
    products = Product.objects.all()[:8]

    context = {'products': products}
    return render(request, 'core/frontpage.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('/')
    else:
        form = SingUpForm()

    context = {'form': form}
    return render(request, 'core/signup.html')

@login_required
def my_account(request):
    return render(request, 'core/myaccount.html')


@login_required
def edit_my_account(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')

        request.user.save()

        return redirect('core:my_account')
    return render(request, 'core/edit_myaccount.html')


def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__slug__icontains=query) 
        )


    context = {
        'products': products, 
        'categories': categories, 
        'active_category': active_category
    }
    return render(request, 'core/shop.html', context)