from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .forms import ProductForm

from django.contrib import messages
from django.views import View
from .models import Product

from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

class CustomerLoginView(View):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            customer = authenticate(request, username=username, password=password)

            if customer is not None:
                login(request, customer)
                return redirect('home')  # Replace 'home' with your home page URL name
            else:
                messages.error(request, 'Invalid username or password')
        return render(request, self.template_name, {'form': form})


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        context = {
            'title': 'Welcome to Our Bakery',
            'message': 'Freshly baked goods made with love!',
            'products': products
        }
        return render(request, 'base.html', context)

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductListView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'product_list.html', {'products': products})

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'product_form.html', {'form': form})

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, 'product_form.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'product_form.html', {'form': form})

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'product_confirm_delete.html', {'product': product})

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product_list')
