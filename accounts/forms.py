from django import forms
from django.forms import  Textarea
from .models import CustomerUser,CredentialCategory,Credential,LoginHistory
from django.utils.translation import gettext_lazy as _
from django.core.validators import  RegexValidator,validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
# from django.db import transaction

phone_regex = r'^\d{10}$'
class AutocompleteEmailField(forms.EmailField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['autocomplete'] = 'email'

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)
    phone_regex = r'^\d{10}$'
    phone = forms.CharField(label="Phone", max_length=10, validators=[
        RegexValidator(
            regex=phone_regex,
            message="Phone number must be 10 digits (e.g., 5551234567).",
        ),
    ])
    email = AutocompleteEmailField()

    class Meta:
        model = CustomerUser
        fields = [
            "category",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "phone",
            "email",
            "country",
            "zipcode",
            
        ]
        labels = {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "phone": "",
            "country": "",
            "zipcode": "",
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["category"].initial = 1
    
        self.fields["country"].required = True
        if self.data.get('category') in ['3', '4', '5', '6']:
            self.fields['username'].required = False
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['phone'].required = False

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("Invalid email address")
        return email

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ["first_name", "last_name", "username", "password1", "password2", "phone", "email","country"]
        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required.")

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        username = cleaned_data.get("username")
        disallowed_usernames = ["test", "testing"]

        if first_name in disallowed_usernames:
            self.add_error("first_name", "This first name is not allowed.")
        if last_name in disallowed_usernames:
            self.add_error("last_name", "This last name is not allowed.")
        if username in disallowed_usernames:
            self.add_error("username", "This username is not allowed.")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data.get('password2'):
            user.set_password(self.cleaned_data["password2"])
        else:
            user.set_password(user.password2)
        if commit:
            user.save()
        return user

class LoginHistoryForm(forms.ModelForm):
    class Meta:
        model = LoginHistory
        fields = ['login_time', 'logout_time']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    country = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'country', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.profile.phone = self.cleaned_data['phone']
        user.profile.country = self.cleaned_data['country']
        if commit:
            user.save()
        return user
#==========================CREDENTIAL FORM================================
class CredentialCategoryForm(forms.ModelForm):  
    class Meta:  
        model = CredentialCategory  
        fields = ['department','category', 'slug','description', 'is_active','is_featured']
        widgets = {
            # Use SelectMultiple below
            "category":forms.SelectMultiple(attrs={'class':'form-control', 'category':'category'}),
            "description": Textarea(attrs={"cols": 40, "rows": 2})
            }

class CredentialForm(forms.ModelForm):  
    class Meta:  
        model = Credential
        fields = ['category','name', 'added_by','slug','user_types','description','password','link_name','link','is_active','is_featured']
        labels={
                'link_name':'username/email',
                'link':'Link/url',
                'user_types':'Specify Who Can Access this Credential?'
        }
        widgets = {
            # Use SelectMultiple below
            "category":forms.SelectMultiple(attrs={'class':'form-control', 'id':'category'}),
            "description": Textarea(attrs={"cols": 40, "rows": 2})
            }


class LoginForm(forms.Form):
    enter_your_username_or_email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","autocomplete": "username email"}))
    enter_your_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    # def clean_enter_your_username_or_email(self):
    #     username_or_email = self.cleaned_data.get('enter_your_username_or_email')
    #     # Add your validation logic for email format here
    #     # For example:
    #     if '@' not in username_or_email:
    #         raise forms.ValidationError("Please enter a valid email address.")
    #     return username_or_email

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('enter_your_username_or_email')
        password = cleaned_data.get('enter_your_password')
        # Add validation for required fields here
        # For example:
        if not username_or_email:
            self.add_error('enter_your_username_or_email', "This field is required.")
        if not password:
            self.add_error('password', "This field is required.")   