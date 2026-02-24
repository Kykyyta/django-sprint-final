"""Представления для приложения blog."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, ProfileUpdateForm
from .mixins import CommentRedirectMixin, OnlyAuthorMixin, ProfileRedirectMixin
from .models import Category, Comment, Post
from .utils import get_published_posts

User = get_user_model()


class PostListView(ListView):
    """Представление для списка постов."""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = 10

    def get_queryset(self):
        """Возвращает опубликованные посты с количеством комментариев."""
        queryset = get_published_posts().order_by('-pub_date')
        queryset = queryset.annotate(comment_count=Count('comment'))
        return queryset


class PostDetailView(DetailView):
    """Представление для детальной страницы поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        """Возвращает пост с учётом прав доступа."""
        post = super().get_object()
        if post.author == self.request.user:
            return post
        return super().get_object(get_published_posts())

    def get_context_data(self, **kwargs):
        """Добавляет форму комментария и список комментариев."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comment.select_related('author')
        return context


class PostCreateView (LoginRequiredMixin, ProfileRedirectMixin, CreateView):
    """Представление для создания поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Устанавливает автором текущего пользователя."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OnlyAuthorMixin, CommentRedirectMixin, UpdateView):
    """Представление для редактирования поста."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostDeleteView(OnlyAuthorMixin, ProfileRedirectMixin, DeleteView):
    """Представление для удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        """Добавляет форму с данными поста для подтверждения удаления."""
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class ProfileDetailView(DetailView):
    """Представление для страницы профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_object(self):
        """Возвращает пользователя по username."""
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        """Добавляет посты пользователя с пагинацией."""
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object).order_by('-pub_date')
        posts = posts.annotate(comment_count=Count('comment'))
        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['profile'] = self.object
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля."""

    model = User
    form_class = ProfileUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Возвращает текущего пользователя."""
        return self.request.user

    def get_success_url(self):
        """Возвращает URL профиля после редактирования."""
        return reverse('blog:profile', args=[self.object.username])


class CommentCreateView(LoginRequiredMixin, CommentRedirectMixin, CreateView):
    """Представление для создания комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        """Устанавливает автора и пост для комментария."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(OnlyAuthorMixin, CommentRedirectMixin, UpdateView):
    """Представление для редактирования комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_object(self, queryset=None):
        """Возвращает комментарий по ID."""
        comment_id = self.kwargs.get('comment_id')
        return get_object_or_404(Comment, id=comment_id)

    def get_context_data(self, **kwargs):
        """Добавляет ID поста в контекст."""
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('post_id')
        return context


class CommentDeleteView(OnlyAuthorMixin, CommentRedirectMixin, DeleteView):
    """Представление для удаления комментария."""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CategoryPostsView(DetailView):
    """Представление для списка постов в категории."""

    model = Category
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_object(self, queryset=None):
        """Возвращает категорию по slug с проверкой публикации."""
        category = get_object_or_404(Category,
                                     slug=self.kwargs['category_slug'])
        if not category.is_published:
            raise Http404("Категория не опубликована")
        return category

    def get_context_data(self, **kwargs):
        """Добавляет посты категории с пагинацией."""
        context = super().get_context_data(**kwargs)
        posts = get_published_posts(self.object.slug).order_by('-pub_date')
        posts = posts.annotate(comment_count=Count('comment'))
        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context
