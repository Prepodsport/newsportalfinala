phyton manage.py shell

from news.models import *

# Создать двух пользователей (с помощью метода User.objects.create_user('username')).

u1 = User.objects.create_user(username='ivan')

u2 = User.objects.create_user(username='max')

# Создать два объекта модели Author, связанные с пользователями.

Author.objects.create(author = u1)

Author.objects.create(author = u2)

# Добавить 4 категории в модель Category.

Category.objects.create(article_category ='EDUCATION')

Category.objects.create(article_category ='SPORT')

Category.objects.create(article_category ='LEISURE')

Category.objects.create(article_category ='ENTERTAINMENTS')

# Добавить 2 статьи и 1 новость.

author = Author.objects.get(id=1)

Post.objects.create(post_author=author, category='A', title='Спорт- это жизнь', content='Очень много текста про спорт')

Post.objects.create(post_author=author, category='A', title='Спорт- это жизнь', content='Очень много текста про образование')

Post.objects.create(post_author=author, category='N', title='Спорт- это жизнь', content='Очень много текста про досуг')

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).

Post.objects.get(id=1).post_category.add(Category.objects.get(id=1))

Post.objects.get(id=1).post_category.add(Category.objects.get(id=4))

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).

Comment.objects.create(comment_post=Post.objects.get(id=1), comment_user=Author.objects.get(id=1).author, feedback_text='коментарий 1')

Comment.objects.create(comment_post=Post.objects.get(id=2), comment_user=Author.objects.get(id=1).author, feedback_text='коментарий 2')

Comment.objects.create(comment_post=Post.objects.get(id=3), comment_user=Author.objects.get(id=2).author, feedback_text='коментарий 3')

Comment.objects.create(comment_post=Post.objects.get(id=1), comment_user=Author.objects.get(id=2).author, feedback_text='коментарий 4')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.

Comment.objects.get(id=1).like()

Post.objects.get(id=1).dislike()

Post.objects.get(id=1).dislike()

Post.objects.get(id=1).dislike()

Post.objects.get(id=1).dislike()

Post.objects.get(id=3).like()

Comment.objects.get(id=1).comment_rate

1

Post.objects.get(id=1).post_rate

-4

# Обновить рейтинги пользователей.

u1 = Author.objects.get(id=1)

u1.update_rating()

u1.user_rate

-8

u2 = Author.objects.get(id=2)

u2.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))

{'comment_rating': 0}

u2.update_rating()

u2.user_rate

0

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).

s = Author.objects.order_by('user_rate')

for i in s:

...     i.user_rate

...     i.author.username

-8

'ivan'

0

'max'

>>>

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.

p = Post.objects.order_by('-post_rate')

for i in p[:1]:

...     i.date_created

...     i.post_author.author

...     i.post_rate

...     i.title

...     i.preview()

datetime.date(2022, 10, 27)

<User: ivan>

1

'Спорт- это жизнь'

'Очень много текста про досуг...'

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

Post.objects.all().order_by('-post_rate')[0].comment_set.values('comment_date_created', 'comment_user', 'comment_rate', 'feedback_text')

<QuerySet [{'comment_date_created': datetime.date(2022, 10, 27), 'comment_user': 2, 'comment_rate': 0, 'feedback_text': 'коментарий 3'}]>
