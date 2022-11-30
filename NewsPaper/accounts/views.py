from django.contrib.auth.models import *
from django.views.generic.edit import *
from .forms import *
from django.contrib.auth.decorators import *
from django.shortcuts import *
from django.contrib.auth.models import *
from django.contrib.auth.mixins import *
from django.urls import *
from news.models import *

from news.models import Author


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


class AccountUserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'news_pages/account_update_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('news_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        context['is_your_id'] = int(self.request.user.id)
        context['path'] = int(self.request.path.split('/')[-1])
        return context


@login_required
def set_me_author(request):
    user = request.user
    author_group = Group.objects.get(name='Authors')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        if not hasattr(user, 'author'):
            Author.objects.create(author=User.objects.get(pk=user.id))

    return redirect('/news/')
