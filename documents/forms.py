from django import forms

from documents.models import Document


class DocumentForm(forms.ModelForm):
    nonce = forms.CharField(required=False)
    hash = forms.CharField(required=False)

    class Meta:
        model = Document
        fields = ['title', 'data', 'nonce', 'hash', ]
