from django import forms
from .models import Order, Feedback1

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'address']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback1
        fields = ['product', 'comment', 'rating']
