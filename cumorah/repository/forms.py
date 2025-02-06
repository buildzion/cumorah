

from django import forms

from cumorah.fields import HtmlTextField
from cumorah.repository.models import NoteComment, DocumentNote


class NoteForm(forms.ModelForm):
    class Meta:
        model = DocumentNote
        fields = [
            'title',
            'reference',
            'note',
        ]

    note = HtmlTextField(required=True)


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = NoteComment
        fields = [
            'comment',
        ]
