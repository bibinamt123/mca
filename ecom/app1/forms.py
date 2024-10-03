from django import forms
from .models import Order, Feedback1
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    pin_code = forms.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'phone_number', 'address', 'pin_code']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'address']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback1
        fields = ['product', 'comment', 'rating']
