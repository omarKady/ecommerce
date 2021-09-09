from django import forms
from django.forms import fields
from .models import Feedback, Order

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'feedback', 'email',)

class MakeOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('address', 'email', 'mobile', 'status',)
