from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *
from .import views

urlpatterns = [
   path("news/", (NewsList.as_view()), name='news_list'),
   path('news/<int:pk>', PostDetail.as_view(), name='news_details'),
   path('search/', PostSearch.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path("articles/create/", ArticlesCreate.as_view(), name='articles_create'),
   path("news/<int:pk>/edit/", NewsUpdate.as_view(), name='news_update'),
   path("articles/<int:pk>/edit/", ArticlesUpdate.as_view(), name='articles_update'),
   path("news/<int:pk>/delete/", NewsDelete.as_view(), name='news_delete'),
   path("articles/<int:pk>/delete/", ArticlesDelete.as_view(), name='articles_delete'),
   path('login/', auth_views.LoginView.as_view(), name='login'),
   path('accounts/password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   path("categories/<int:pk>", CategoriesView.as_view(), name='categories_list'),
   path('categories/<int:pk>/subscribe/', add_me_to_category, name='sub_category'),
   path('categories/', cache_page(60 * 5)(CategoryListView.as_view()), name='category_lists'),

]