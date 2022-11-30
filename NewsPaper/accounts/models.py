from django.db import models
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        author_group = Group.objects.get(name='Authors')
        author_group.user_set.add(user)
        return user
