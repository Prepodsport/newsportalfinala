from django.views.generic import ListView, DetailView
from .models import Post, PostCategory
from datetime import datetime, timezone


class PostsList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'


    def get_context_data(self, **kwargs):
        # распаковываем self = Posts
        context = super().get_context_data(**kwargs)
        context['categories'] = PostCategory.objects.all()
        return context

    def get_queryset(self):
        qset = super().get_queryset()
        return qset.order_by('id','-date_created')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/news_detalis.html'
    queryset = Post.objects.all()