from django import forms
from .models import User,UserCategory
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "password1",
            "password2",
            "email",
            "phone",
            "gender",
        ]
        labels = {
            "first_name": "",
            "last_name": "",
            # "password1": "",
            # "password2": "",
            "email": "",
            "gender": "",
            "phone": "",
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['category'].required= True
        # set category initial=1 and added category
        # self.fields["category"].initial = 1
        # self.fields["sub_category"].initial = 1
        # self.fields["gender"].required = True
        # self.fields["country"].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    # username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class UserCategoryForm(forms.Form):
    class Meta:
        model = UserCategory
        fields = [
            "category",
            "sub_category",
        ]
        labels = {
            "category": "Category",
            "sub_category": "Sub Category",
        }

    # def __init__(self, *args, **kwargs):
    #     super(UserCategoryForm, self).__init__(*args, **kwargs)
    #     # self.fields['category'].required= True
    #     # set category initial=1 and added category