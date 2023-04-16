from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostList, PostDetail, PostSearch, NewsCreate, \
   ArticlesCreate, PostUpdate, PostDelete, CategoryListView, subscribe

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>',  cache_page(60*10)(PostDetail.as_view()), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
