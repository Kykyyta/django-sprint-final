"""Миксины для блога."""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин для проверки авторства."""

    def test_func(self):
        """Проверяет, является ли пользователь автором."""
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        """Перенаправляет на страницу поста при отсутствии прав."""
        post_id = self.kwargs.get('post_id')
        return redirect(reverse_lazy('blog:post_detail',
                                     kwargs={'post_id': post_id}))


class CommentRedirectMixin:
    """Миксин для перенаправления после комментария."""

    def get_success_url(self):
        """Возвращает URL страницы поста."""
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})


class ProfileRedirectMixin:
    """Миксин для перенаправления в профиль."""

    def get_success_url(self):
        """Возвращает URL страницы профиля."""
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})
