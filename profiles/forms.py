from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=140)
    first_name =forms.CharField(max_length=140)
    last_name= forms.CharField(max_length=140)
    email=forms.EmailField(required=False)
 

    class Meta:
        model = Profile
        fields = ["username","Image"]

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

        