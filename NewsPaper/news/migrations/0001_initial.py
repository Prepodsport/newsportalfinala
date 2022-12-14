# Generated by Django 4.1.2 on 2022-11-28 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_rate', models.BigIntegerField(default=0, verbose_name='Рейтинг автора')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_category', models.CharField(max_length=64, unique=True, verbose_name='Название категории')),
                ('subscribers', models.ManyToManyField(related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('A', 'Статья'), ('N', 'Новость')], default='N', max_length=2, verbose_name='Тип поста')),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='Дата создания поста')),
                ('title', models.CharField(max_length=128, verbose_name='Название поста')),
                ('content', models.TextField(verbose_name='текст поста')),
                ('post_rate', models.SmallIntegerField(default=0, verbose_name='Рейтинг поста')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Категория')),
                ('post_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Пост с категориями',
                'verbose_name_plural': 'Посты с категориями',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='post_category',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category', verbose_name='Категория поста'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_text', models.TextField(verbose_name='Текст комментария')),
                ('comment_date_created', models.DateField(auto_now_add=True, verbose_name='Дата создания комментария')),
                ('comment_rate', models.IntegerField(default=0, verbose_name='Рэйтинг комментария')),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post', verbose_name='Пост')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]
