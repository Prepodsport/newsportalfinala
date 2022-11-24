from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
#from datetime import datetime, timezone
from .search import PostFilter
from django.core.paginator import Paginator
from django.shortcuts import render
from .filters import PostFilter
from .forms import NewsCreateForm, ArticlesCreateForm
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache


class NewsList(ListView):
    model = Post
    ordering = "-date_created"
    template_name = 'flatpages/news.html'
    context_object_name = 'news_list'
    paginate_by = 2
    #form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PostCategory.objects.all()
        return context

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


class NewsCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    model = Post
    form_class = NewsCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = "N"
        post.post_author = Author.objects.get(author=str(self.request.user.id))
        post.save()
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    model = Post
    form_class = ArticlesCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category = "A"
        post.post_author = Author.objects.get(author=str(self.request.user.id))
        post.save()
        return super().form_valid(form)

#class PostUpdate(UpdateView):
   # template_name = 'flatpages/news_create.html'
   # form_class = PostForm
    #model = Post

    #def get_object(self, **kwargs):
        #id = self.kwargs.get('pk')
        #return Post.objects.get(pk=id)
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    model = Post
    form_class = NewsCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.change_post',)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    raise_exception = True
    model = Post
    form_class = NewsCreateForm
    template_name = 'flatpages/news_create.html'
    permission_required = ('news.change_post',)

# дженерик для удаления новости
class NewsDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    model = Post
    template_name = 'flatpages/news_delete.html'
    #form_class = PostForm
    queryset = Post.objects.all()
    success_url = reverse_lazy ('news_list')
    permission_required = ('news.delete_post',)

class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    raise_exception = True
    model = Post
    template_name = 'flatpages/news_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy ('news_list')
    permission_required = ('news.delete_post',)


class CategoriesView(ListView):
    model = Post
    template_name = 'flatpages/news_categories_view.html'
    context_object_name = "categories_list"
    paginate_by = 10

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'flatpages/news_categories_list_view.html'
    context_object_name = "categories_list"


@login_required
def add_me_to_category(request, pk):
    user = request.user
    post_category = Category.objects.get(pk=pk)
    post_category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    # return redirect('categories_list', category)
    return render(request,'flatpages/subscribe.html', {'category': post_category, 'message': message})