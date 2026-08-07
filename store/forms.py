import re
from django import forms
from django.contrib.auth.models import User
from .models import Order


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "address",
            "city",
            "phone",
        ]

    def clean_full_name(self):
        name = self.cleaned_data["full_name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Full name must contain at least 3 characters."
            )

        return name

    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if len(address) < 10:
            raise forms.ValidationError(
                "Please enter a complete address."
            )

        return address

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not re.fullmatch(r"\d{11}", phone):
            raise forms.ValidationError(
                "Phone number must contain exactly 11 digits."
            )

        return phone
