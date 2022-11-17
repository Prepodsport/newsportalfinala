from django.forms import ModelForm, BooleanField
from .models import *
from django import forms


# class PostForm(ModelForm):
# check_box = BooleanField(label='Поставь галочку')

# class Meta:
# model = Post
# fields = ['title',   'post_author',
# 'post_category', 'content', 'check_box']


class newsCreateForm(forms.ModelForm):
    check_box = BooleanField(label='Поставь галочку')

    class Meta:
        model = Post

        fields = [
            'title',
            'content',
            'post_author',
            #'post_category',
            'check_box',
        ]


class articlesCreateForm(forms.ModelForm):
    check_box = BooleanField(label='Поставь галочку')

    class Meta:
        model = Post

        fields = [
            'title',
            'content',
            'post_author',
            #'post_category',
            'check_box',
        ]
