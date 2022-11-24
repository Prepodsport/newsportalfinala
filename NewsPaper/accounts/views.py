from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from ..news.models import Author


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


@login_required
def set_me_author(request):
    user = request.user
    author_group = Group.objects.get(article_category='author')
    if not request.user.groups.filter(article_category='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(post_author=user)

    return redirect('/news/')
