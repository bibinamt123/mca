import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Product, Order, Feedback1,Payment,UserProfile
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

def order_product(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('initiate_payment', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'order_product.html', {'form': form})


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


def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    amount = int(order.product.price * order.quantity * 100)  # Convert to paise

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency='INR',
        payment_capture='1'
    ))

    # Save the payment details in the database
    payment = Payment.objects.create(
        order=order,
        user=request.user,
        amount=order.product.price * order.quantity,
        razorpay_order_id=razorpay_order['id']
    )

    context = {
        'order': order,
        'payment': payment,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZORPAY_KEY_ID,
        'amount': amount,
        'currency': 'INR'
    }

    return render(request, 'payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'Paid'
            payment.save()

            # Redirect to the home page after successful payment
            return redirect('home')
        except Payment.DoesNotExist:
            return HttpResponse("Payment not found.")
    
    return redirect('home')