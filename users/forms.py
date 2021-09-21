from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
customUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='EMAIL')
    first_name = forms.CharField(max_length=50) # to be required
    last_name = forms.CharField(max_length=50) # to be required
    phone = forms.CharField(max_length=50, label='Phone Number')
    # , error_message = {'exists' : 'This Email Already Exists'}
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'age', 'phone', 'first_name', 'last_name')
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        if customUser.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError("Error This Email Already exists ...")
            #raise ValidationError(self.fields['email'].error_message['exists'])
        return self.cleaned_data['email']
    
    def clean_phone(self):
        if customUser.objects.filter(phone=self.cleaned_data['phone']).exists():
            raise ValidationError("Error this phone already exists ...")
        return self.cleaned_data['phone']
    
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)