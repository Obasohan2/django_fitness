from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['height_cm','weight_kg','goals','exercise_plans','nutrition_plans']
        widgets = {
            'goals': forms.Textarea(attrs={'rows':3})
        }