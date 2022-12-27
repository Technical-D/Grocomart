from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from app.models import Customer, Newsletter, Queries

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid Email Address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    mobile = forms.CharField(max_length=12)


    class Meta:
        model = Customer
        fields = ('first_name','last_name','email', 'mobile', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            customer = Customer.objects.get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.')

    

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Customer
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login!")


class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid Email.')
    
    class Meta:
        model = Newsletter
        fields = ('email',)

class QueriesForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=60)
    subject = forms.CharField(max_length=60)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Queries
        fields = ('name', 'email', 'subject', 'message',)