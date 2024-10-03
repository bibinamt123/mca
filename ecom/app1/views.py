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

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def proceed_to_payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate the total amount for display (in INR)
    total_amount_display = sum(item.product.price * item.quantity for item in cart_items)  # Amount in INR

    if request.method == "POST":
        # Create a new order in Razorpay (convert to paise)
        total_amount = int(total_amount_display * 100)  # Amount in paise for Razorpay

        order_data = {
            'amount': total_amount,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1',  # Auto capture
        }
        order = razorpay_client.order.create(data=order_data)
        
        # Render the payment page with the order details
        return render(request, 'payment.html', {
            'order_id': order['id'], 
            'total_amount': total_amount_display  # Use the display amount (not converted to paise)
        })

    return render(request, 'proceed_to_payment.html', {'total_amount': total_amount_display})



@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        # Get the payment details
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature,
        }

        try:
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If verification is successful, you can proceed to mark the order as paid
            # (e.g., updating the order status in your database)

            # Clear the cart after successful payment
            Cart.objects.filter(user=request.user).delete()

            # Redirect to the home page or a success page
            return redirect('home')  # Replace 'home' with your home URL name

        except Exception as e:
            # Handle payment verification failure
            return render(request, 'payment_failed.html', {'error': str(e)})

    return render(request, 'payment_failed.html')