from django.contrib.auth import logout, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.defaultfilters import register
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DeleteView, UpdateView, DetailView
import pandas as pd

from .forms import *
from .models import *


@register.filter(name='split')
def split(value, key):
    return value.split(key)


class UserDetailView(UserPassesTestMixin, DetailView):
    model = User
    template_name = 'dataset/user_profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'

    def test_func(self):
        user = self.get_object()
        return self.request.user.is_authenticated \
            and (self.request.user.is_superuser or user.pk == self.request.user.pk)


class IntroView(TemplateView):
    template_name = 'dataset/intro.html'


class DatasetListView(UserPassesTestMixin, ListView):
    paginate_by = 4
    model = Dataset
    template_name = 'dataset/dataset_list.html'
    context_object_name = 'datasets'
    ordering = ['-modified_date']
    raise_exception = True

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DatasetDetailView(UserPassesTestMixin, DetailView):
    model = Dataset
    template_name = 'dataset/dataset.html'
    pk_url_kwarg = 'dataset_id'
    context_object_name = 'dataset'

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table_data = pd.read_table(context['dataset'].file)
        context['df'] = table_data

        return context


class DatasetSearchView(UserPassesTestMixin, ListView):
    model = Dataset
    template_name = 'dataset/dataset_list.html'
    context_object_name = 'datasets'

    def test_func(self):
        return self.request.user.is_authenticated

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Dataset.objects.filter(Q(file__icontains=query) | Q(description__icontains=query))
        else:
            return Dataset.objects.all()


class DatasetCreateView(UserPassesTestMixin, CreateView):
    form_class = DatasetForm
    template_name = 'dataset/dataset_add.html'

    raise_exception = True

    def get_success_url(self):
        return reverse('dataset', kwargs={'dataset_id': self.object.pk})

    def form_valid(self, form):
        dataset_req = form.save(commit=False)
        dataset_req.user = self.request.user
        dataset_req.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_authenticated


class DatasetDeleteView(UserPassesTestMixin, DeleteView):
    model = Dataset
    success_url = reverse_lazy('dataset_list')
    raise_exception = True

    def test_func(self):
        dataset = self.get_object()
        return self.request.user.is_authenticated \
            and (self.request.user.is_superuser or dataset.user == self.request.user)


class DatasetUpdateView(UserPassesTestMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    template_name = 'dataset/dataset_update.html'
    context_object_name = 'dataset'

    def get_success_url(self):
        return reverse('dataset', kwargs={'dataset_id': self.object.pk})

    def test_func(self):
        dataset = self.get_object()
        return self.request.user.is_authenticated \
            and (self.request.user.is_superuser or dataset.user == self.request.user)


class RegisterUserView(UserPassesTestMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'dataset/auth/register.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        return not self.request.user.is_authenticated

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dataset_list')


class LoginUserView(UserPassesTestMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'dataset/auth/login.html'

    def test_func(self):
        return not self.request.user.is_authenticated

    def get_success_url(self):
        return reverse_lazy('dataset_list')


def logout_user(request):
    logout(request)
    return redirect('login')


def tr_handler404(request, exception):
    """
    404 Error handler
    """
    return render(request=request, template_name='dataset/exceptions/error_page.html', status=404, context={
        'title': 'Page not found: 404',
        'error_message': 'Unfortunately, such a page was not found, or was moved',
    })


def tr_handler500(request):
    """
    500 Error handler
    """
    return render(request=request, template_name='dataset/exceptions/error_page.html', status=500, context={
        'title': 'Server error: 500',
        'error_message': 'Internal site error, go back to the home page, '
                         'we will send an error report to the site administration',
    })


def tr_handler403(request, exception):
    """
    403 Error handler
    """
    if request.user.is_authenticated:
        return redirect('dataset_list')
    else:
        return redirect('login')


def tr_handler405(request, exception):
    """
    405 Error handler
    """
    if request.user.is_authenticated:
        return redirect('dataset_list')
    else:
        return redirect('login')
