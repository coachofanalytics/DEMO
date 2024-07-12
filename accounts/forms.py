from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
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
    phone_regex = r'^\d{10}$'
  

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
            "phone",
            "gender",
            "email",
            "address",
            "city",
            "state",
            "country",
            "zipcode",
            "resume_file",
            "is_staff",
            "is_applicant",
        ]
        labels = {
            "sub_category": "",
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "gender": "",
            "phone": "",
            "address": "",
            "city": "",
            "state": "",
            "country": "",
            "zipcode": "",
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["category"].initial = 1
        self.fields["sub_category"].initial = 1
        self.fields["gender"].required = True
        self.fields["country"].required = True
        if self.data.get('category') in ['3', '4', '5', '6']:
            self.fields['username'].required = False
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['gender'].required = False
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
                validate_email(email) # type: ignore
            except forms.ValidationError:
                raise forms.ValidationError("Invalid email address")
        return email

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ["first_name", "last_name", "username", "password1", "password2", "phone", "email", "gender", "country"]
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