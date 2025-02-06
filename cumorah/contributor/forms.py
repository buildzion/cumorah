
from django import forms

from cumorah.contributor import models


class RequestActivationForm(forms.ModelForm):
    display_name = forms.CharField(required=True)
    bio = forms.CharField(required=True, help_text="Provide some basic information about yourself to share publicly")
    activation_request_notes = forms.CharField(required=True, widget=forms.Textarea)

    class Meta:
        model = models.Contributor
        fields = [
            'display_name',
            'bio',
            'activation_request_notes',
        ]


class ContributorUpdateForm(forms.ModelForm):
    active = forms.BooleanField(required=False, help_text="Check this box to approve this contributor")

    class Meta:
        model = models.Contributor
        fields = [
            'display_name',
            'bio',
            'level',
            'active',
        ]
