from django.core.exceptions import ValidationError
from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'newsArticle', 'category', 'title', 'text']

    def clean(self):
        cleaned = super().clean()
        title = cleaned.get("title")
        text = cleaned.get("text")

        if title == text:
            raise ValidationError("The title should not be identical to the content of the article or news")
        return cleaned

