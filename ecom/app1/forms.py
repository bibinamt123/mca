from django import forms
from .models import Order, Feedback

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'address']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['product', 'comment', 'rating']
