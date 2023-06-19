from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import BaseRegisterForm, BaseUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class BaseUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = BaseUpdateForm
    success_url = '/sign/<int:pk>/profile'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
