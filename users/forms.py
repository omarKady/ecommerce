from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
customUser = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    #age = forms.IntegerField(required=True)
    email = forms.EmailField(required=True, label='EMAIL')
    # , error_message = {'exists' : 'This Email Already Exists'}
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'age',)
    
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
    
    
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)