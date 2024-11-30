from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.core.validators import validate_email

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or E-mail")
    remember_me = forms.BooleanField(required=False, label="Keep me signed in")


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomerUser
        fields = [
            "category",
            "sub_category",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
            "email",
            "is_staff",
        ]
        labels = {
            "sub_category": "",
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].initial = 1
        self.fields["sub_category"].initial = 1
        category = self.data.get('category')
        if category in ['3', '4', '5', '6']:
            self.fields['username'].required = False
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")

        # Validate passwords match
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords don't match.")

        # Validate email format
        if email:
            try:
                validate_email(email)
            except forms.ValidationError:
                self.add_error("email", "Invalid email address.")

        # Check for disallowed names
        disallowed_names = ["test", "testing"]
        for field in ["first_name", "last_name", "username"]:
            value = cleaned_data.get(field, "").lower()
            if value in disallowed_names:
                self.add_error(field, f"This {field.replace('_', ' ')} is not allowed.")

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password2')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForms(forms.Form):
    # username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
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

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = MemberRegistration
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone_number', 'country', 'city', 'agree']
        widgets = {
            'gender': forms.RadioSelect(choices=MemberRegistration.GENDER_CHOICES),
            'agree': forms.CheckboxInput()
        }
        labels = {
            'agree': 'I agree to the terms and conditions'
        }