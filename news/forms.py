from django import forms

from .models import Post, Comment, NewsLetter, Code


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        # поле author-текущий пользователь уже добавлено
        # при переопределении form_valid в NewsCreate
        fields = [
            'category_news',
            'title',
            'text',
            'upload',
            ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # поля commentUser - текущий пользователь, commentPost уже добавлены
        # при переопределении form_valid в CommentCreate
        fields = [
            'text',
            ]


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        # поле user-текущий пользователь уже добавлено
        # при переопределении form_valid
        fields = [
            'title',
            'text',
        ]


class ConfirmationCodeForm(forms.ModelForm):

    class Meta:
        model = Code
        fields = [
            'code_entered',
            ]
