"""Обработчики страниц и ошибок для приложения pages."""

from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Представление для страницы 'О проекте'."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """Представление для страницы 'Правила'."""

    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Обработчик ошибки 404 (страница не найдена)."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Обработчик ошибки 403 CSRF (недействительный CSRF-токен)."""
    return render(request, 'pages/403csrf.html', status=403)


def internal_server_error(request):
    """Обработчик ошибки 500 (внутренняя ошибка сервера)."""
    return render(request, 'pages/500.html', status=500)
