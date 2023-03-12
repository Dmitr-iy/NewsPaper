
from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'heads.html'
    context_object_name = 'titles'

class PostDetail(DetailView):
    model = Post
    template_name = 'head.html'
    context_object_name = 'title'
