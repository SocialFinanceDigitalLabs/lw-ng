from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.models import YoungPerson


# Create your forms here.

class NewYoungPersonForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    
    def save(self, commit=True):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user = User.objects.create(username = f"{first_name}.{last_name}", first_name = first_name, last_name = last_name)
        yp = YoungPerson.objects.create(user = user)
        return yp