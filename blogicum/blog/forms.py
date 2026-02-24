"""Формы для приложения blog."""

from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post

User = get_user_model()


class PostForm(forms.ModelForm):
    """Форма для создания и редактирования постов."""

    class Meta:
        """Метаданные формы поста."""

        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class ProfileUpdateForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        """Метаданные формы профиля."""

        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев."""

    class Meta:
        """Метаданные формы комментария."""

        model = Comment
        fields = ('text',)
