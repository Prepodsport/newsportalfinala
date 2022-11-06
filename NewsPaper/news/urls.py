from django.urls import path
from .views import PostsList, PostDetail
from .import views

urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>/', PostDetail.as_view(), name='news_details'),
]