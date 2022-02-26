from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """Form for newsletter subscription by Email"""
    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(attrs={"class": " editContent", "placeholder": " Your Email..."})
        }
        labels = {
            "email": ''
        }

