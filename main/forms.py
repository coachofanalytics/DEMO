from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomerUser
from django.utils.translation import gettext_lazy as _
# from django.db import transaction

class RegistrationForm(forms.ModelForm):
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
            "phone",
            "gender",
            "email",
            "address",
            "city",
            "state",
            "country",
            "resume_file",
            "is_employee",
            "is_applicant",
        ]
        labels = {
                    "sub_category": "sub_category",
                    "first_name": "first_name",
                    "last_name": "last_name",
                    "username": "username",
                    "email": "email",
                    "gender": "gender",
                    "phone": "phone",
                    "address": "address",
                    "city": "city",
                    "state": "state",
                    "country": "country",
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # self.fields['category'].required= True
        # set category initial=1 and added category
        self.fields["category"].initial = 1
        self.fields["sub_category"].initial = 1
        self.fields["gender"].required = True
        self.fields["country"].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

class ContactForm(forms.ModelForm):
    class Meta:
        # model = DSU
        fields = [
            "trained_by",
            "client_name",
            "type",
            "category",
            "task",
            "plan",
            "challenge",
            "uploaded",
        ]
        labels = {
            "type": "Are You a Client/Staff?(Select Other if None of the above)",
            "client_name": "Manager",
            "trained_by": "Staff/Employee",
            "category": "Pick your Category</h2>",
            "task": "What Did You Work On?",
            "plan": "What is your next plan of action on areas that you have not touched on?",
            "challenge": "How Can We Help You?",
            "uploaded": "Have you uploaded any DAF evidence/1-1 sessions?",
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['trained_by'].required=False
        self.fields['client_name'].required=False
        self.fields['type'].required=False
        self.fields['category'].required=False
        self.fields['task'].required=False
        self.fields['plan'].required=False
        self.fields['challenge'].required=False