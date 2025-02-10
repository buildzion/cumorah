
from django import forms

from cumorah.contributor import models
from cumorah.fields import HtmlTextField


class RequestActivationForm(forms.ModelForm):
    display_name = forms.CharField(required=True)
    bio = HtmlTextField(required=True,
                        help_text="Provide some basic information about yourself to share publicly")
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
    bio = HtmlTextField(required=True,
                        help_text="Provide some basic information about yourself to share publicly")

    class Meta:
        model = models.Contributor
        fields = [
            'display_name',
            'bio',
            'level',
            'active',
        ]
