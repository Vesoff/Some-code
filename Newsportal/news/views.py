from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, resolve
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


class PList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PSearchList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'create.html'


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post',
                           'news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',
                           'news.change_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_search')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post')
    model = Post
    form_class = PostForm
    template_name = 'create_art.html'

    def form_valid(self, form):
        form.instance.post_type = 'article'
        return super().form_valid(form)


class PostCategory(ListView):
    model = Post
    template_name = 'category.html'
    context_object_name = 'post'
    ordering = ['-time_in']
    paginate_by = 10

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(category=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        subscribed = category.subscribers.filter(email=user.email)
        if not subscribed:
            context['category'] = category

        return context


def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribed.html',
            {
                'category': category,
                'user': user,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'{category} subscription',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email,],
        )
        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('personal')
    return redirect(request.META.get('HTTP_REFERER'))
