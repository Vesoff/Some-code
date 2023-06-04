from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(field_name='time_in', widget=forms.DateInput(attrs={'type': 'date'}), label='Поиск по дате',
                      lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
        }
