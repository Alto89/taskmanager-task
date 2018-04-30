# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from .form import TaskCreateForm, SubTaskCreateForm, RegisterForm
from .models import Profile, Task, SubTask
# Create your views here.

User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return render(request, "home.html", {})

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'taskmanager/user.html'
    
    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        user = self.get_object()
        #query = self.request.GET.get('q')  # todo:  wtf?

        task_exists = SubTask.object.filter(assigned=user).exists()
        qs = Task.objects.filter(assigned=self.get_object())
        if task_exists and qs.exists():
            context['tasks'] = qs
        return context

class TaskListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Task.objects.filter(assigned=self.request.user)

class TaskUpdateView():
    form_class = TaskCreateForm
    template_name = 'taskmanager/detail-update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        return Task.objects.filter(assigned=self.request.user)


class SubTaskListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return SubTask.objects.filter(assigned=self.request.user)
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = 'task_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        return super(TaskCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(TaskCreateView, self).get_context_data(*args, **kwargs)
        return context


class SubTaskCreateView(LoginRequiredMixin, CreateView):
    form_class = SubTaskCreateForm
    template_name = 'task_form.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        return super(SubTaskCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(SubTaskCreateView, self).get_context_data(*args, **kwargs)
        return context

class SubTaskUpdateView():
    form_class = SubTaskCreateForm
    template_name = 'taskmanager/detail-update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SubTaskUpdateView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        return SubTask.objects.filter(assigned=self.request.user)