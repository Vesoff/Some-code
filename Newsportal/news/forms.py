from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django_filters import DateFilter


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=3)
    time_post = DateFilter(field_name='time_in', widget=forms.DateInput(attrs={'type': 'date'}), label='Поиск по дате',
                           lookup_expr='date__gte')

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 10:
            raise ValidationError({
                "text": "Содержание не может быть менее 10 символов."
            })
        return cleaned_data
