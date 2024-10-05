import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Product, Order, Feedback1,Payment,UserProfile,Cart
from .forms import OrderForm, FeedbackForm,CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Save additional fields in UserProfile
            phone_number = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')
            pin_code = form.cleaned_data.get('pin_code')

            UserProfile.objects.create(
                user=user, 
                phone_number=phone_number,
                address=address,
                pin_code=pin_code
            )

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# def order_product(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)  # Don't save to the database yet
#             order.user = request.user  # Set the user field to the current user
#             order.save()  # Now save to the database
#             return redirect('home')
#     else:
#         form = OrderForm()
#     return render(request, 'order_product.html', {'form': form})

# def order_product(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()
#             return redirect('initiate_payment', order_id=order.id)
#     else:
#         form = OrderForm()
#     return render(request, 'order_product.html', {'form': form})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('product_list')

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'view_cart.html', {'cart_items': cart_items})

def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        if quantity > 0:
            cart_item.quantity = quantity+1
            cart_item.save()
        return redirect('view_cart')

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assign the logged-in user
            feedback.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def user_feedbacks(request):
    feedbacks = Feedback1.objects.filter(user=request.user)
    return render(request, 'user_feedbacks.html', {'feedbacks': feedbacks})

def feedback_success(request):
    return render(request, 'feedback_success.html')


def total_orders_view(request):
    total_orders = Order.objects.count()
    return render(request, 'total_orders.html', {'total_orders': total_orders})

def delivery_address(request):
    cart_items = Cart.objects.filter(user=request.user)

    if request.method == 'POST':
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        pin_code = request.POST.get('pin_code')

        # Create an order for each cart item
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                address=address,
                phone_number=phone_number,
                pin_code=pin_code
            )

        return redirect('proceed_to_payment')  # Redirect to the payment page

    return render(request, 'delivery_address.html')


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def proceed_to_payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total amount in INR
    total_amount_display = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        total_amount = int(total_amount_display * 100)  # Convert to paise for Razorpay

        # Create an order in Razorpay
        order_data = {
            'amount': total_amount,
            'currency': 'INR',
            'payment_capture': '1',
        }
        razorpay_order = razorpay_client.order.create(data=order_data)

        # Render payment page with Razorpay order details
        return render(request, 'payment.html', {
            'order_id': razorpay_order['id'],
            'total_amount': total_amount_display
        })

    return render(request, 'proceed_to_payment.html', {'total_amount': total_amount_display})



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
            # Clear the cart after payment success
            Cart.objects.filter(user=request.user).delete()

            return redirect('home')
        except:
            return render(request, 'payment_failed.html')

    return render(request, 'payment_failed.html')