from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from datetime import datetime, timezone
from .search import PostFilter
from django.core.paginator import Paginator
from django.shortcuts import render
from .filters import PostFilter
from .forms import newsCreateForm, articlesCreateForm
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache


class news(ListView):
    model = Post
    ordering = "-date_created"
    template_name = 'flatpages/news.html'
    context_object_name = 'newss'
    paginate_by = 2
    #form_class = PostForm

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        #context['categories'] = PostCategory.objects.all()
       # return context

    #def get_queryset(self):
        #qset = super().get_queryset()
        #return qset.order_by('id','-date_created')

    #def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        #if form.is_valid():
        #    form.save()
        #return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/news_detalis.html'
    context_object_name = "news"
    #queryset = Post.objects.all()
    def get_object(self, *args, **kwargs):
        obj = cache.get(f"news-{self.kwargs['pk']}", None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f"news-{self.kwargs['pk']}", obj)

        return obj
#class PostCreate(CreateView):
    #template_name = 'flatpages/news_create.html'
    #form_class = PostForm

class PostSearch(ListView):
    model = Post
    ordering = "-date_created"
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news_search'
    paginate_by = 4
    #form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = PostFilter(
            self.request.GET,
            queryset=self.get_queryset()
        )
        context['categories'] = PostCategory.objects.all()
        #context['form'] = PostForm()
        return context


class newsCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = newsCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = "N"
        post.post_author = Author.objects.get(author=str(self.request.user.id))
        return super().form_valid(form)

class articlesCreate(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = articlesCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = "A"
        post.post_author = Author.objects.get(author=str(self.request.user.id))
        return super().form_valid(form)
#class PostUpdate(UpdateView):
   # template_name = 'flatpages/news_create.html'
   # form_class = PostForm
    #model = Post

    #def get_object(self, **kwargs):
        #id = self.kwargs.get('pk')
        #return Post.objects.get(pk=id)
class newsUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = newsCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.change_post')


class articlesUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = newsCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.change_post')

# дженерик для удаления новости
class newsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    #form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/news/'

class articlesDelete(DeleteView):
    model = Post
    template_name = 'flatpages/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'