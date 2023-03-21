from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import *
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'heads.html'
    context_object_name = 'titles'
    paginate_by = 2

class PostDetail(DetailView):
    model = Post
    template_name = 'head.html'
    context_object_name = 'title'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateTime')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.quantity = 'News'
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class ArticlesCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'
    def form_valid(self, form):
        post = form.save(commit=False)
        post.quantity = 'Article'
        return super().form_valid(form)

