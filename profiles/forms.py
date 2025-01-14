from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=140)

    class Meta:
        model = Profile
        fields = ["username","Image"]

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['username'].initial = user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            profile.save()
        return profile

        