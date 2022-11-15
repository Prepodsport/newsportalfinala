from django.urls import path
from .views import *
from .import views

urlpatterns = [
   path("news/", (news.as_view()), name='news'),
   path('news/<int:pk>', PostDetail.as_view(), name='news_details'),
   path('search/', PostSearch.as_view(), name='news_search'),
   path('news/create/', newsCreate.as_view(), name='news_create'),
   path("articles/create/", articlesCreate.as_view(), name='articles_create'),
   path("news/<int:pk>/edit", newsUpdate.as_view(), name='news_update'),
   path("articles/<int:pk>/edit", articlesUpdate.as_view(), name='articles_update'),
   path("news/<int:pk>/delete", newsDelete.as_view(), name='news_delete'),
   path("articles/<int:pk>/delete", articlesDelete.as_view(), name='articles_delete'),
]