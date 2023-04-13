from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import *
from .models import Post, Category
from django.contrib.auth.mixins import PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'news/heads.html'
    context_object_name = 'titles'
    paginate_by = 2


class PostDetail(DetailView):
    model = Post
    template_name = 'news/head.html'
    context_object_name = 'title'


class PostSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateTime')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.quantity = 'News'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'title'


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news/article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.quantity = 'Article'
        return super().form_valid(form)


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-dateTime')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'You have subscribed to the newsletter and articles of the category'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
