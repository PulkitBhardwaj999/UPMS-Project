from dataclasses import fields
from unicodedata import name
from django import forms

from .models import Drives

class DriveForm(forms.ModelForm):

    class Meta:
        model = Drives
        fields = '__all__'