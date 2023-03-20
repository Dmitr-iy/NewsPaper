from django.forms import DateInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter, ModelMultipleChoiceFilter

from .models import Post, Author


class PostFilter(FilterSet):
    title = CharFilter('title', label='The title contains', lookup_expr='icontains')
    author = ModelChoiceFilter(field_name='author', label='Author', lookup_expr='exact', queryset=Author.objects.all())
    dateTime = DateFilter(field_name='dateTime', widget=DateInput(attrs={'type': 'date'}), lookup_expr='date', label='dates later')


    class Meta:
        model = Post
        fields = []
