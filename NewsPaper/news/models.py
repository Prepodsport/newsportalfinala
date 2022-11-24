from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    user_rate = models.BigIntegerField(default=0, verbose_name='Рейтинг автора')
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')

    def update_rating(self):
        sum_rating = self.post_set.aggregate(post_rating=Sum('post_rate'))
        result_sum_rating = 0
        try:
            result_sum_rating += sum_rating.get('post_rating')
        except TypeError:
            result_sum_rating = 0

        sum_comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
        result_sum_comment_rating = 0
        result_sum_comment_rating += sum_comment_rating.get('comment_rating')

        self.user_rate = result_sum_rating * 3 + result_sum_comment_rating
        self.save()

    def __str__(self):
        return f"{self.author.username}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    article_category = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.article_category}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    post_category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория поста')

    ARTICLE = 'A'
    NEWS = 'N'
    POSITIONS = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    category = models.CharField(max_length=2, choices=POSITIONS, default=NEWS, verbose_name='Тип поста')
    date_created = models.DateField(auto_now_add=True, verbose_name='Дата создания поста')
    title = models.CharField(max_length=128, verbose_name='Название поста')
    content = models.TextField(verbose_name='Текст поста')
    post_rate = models.SmallIntegerField(default=0, verbose_name='Рейтинг поста')

    def __str__(self):
        return f"ID: {self.id}, title: {self.title}, Author: {self.author.author.username}"

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

    # def get_absolute_url(self):
    # return f'/news/{self.id}'

    def get_absolute_url(self):
        return reverse('news_details', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.post_category.title} | {self.category_category.article_category}'

    class Meta:
        verbose_name = "Пост с категориями"
        verbose_name_plural = "Посты с категориями"


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    feedback_text = models.TextField(verbose_name='Текст комментария')
    comment_date_created = models.DateField(auto_now_add=True, verbose_name='Дата создания комментария')
    comment_rate = models.IntegerField(default=0, verbose_name='Рэйтинг комментария')

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()

    def __str__(self):
        return f'ID comment: {self.id}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
