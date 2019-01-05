from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone
from django.db import IntegrityError
# Create your views here.
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    #products = Product.objects
    products = Product.objects.order_by('-pub_date')
    return render(request, 'products/home.html', {'products':products})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['url']:
            product = Product()
            product.title = request.POST['title']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            #product.image = request.FILES['image']
            product.image = request.FILES['image'] if 'image' in request.FILES else False
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('home')
        else:
            return render(request, 'products/create.html', {'error':'All fields are required.'})
    else:
        return render(request, 'products/create.html')

@login_required(login_url="/accounts/login")
def profile(request):
    user = request.user
    user_posts = Product.objects.filter(hunter=request.user).order_by('-pub_date')
    return render(request, 'products/profile.html', {'user_posts':user_posts, 'user':user})


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product':product})