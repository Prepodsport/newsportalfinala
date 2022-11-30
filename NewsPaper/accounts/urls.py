from django.urls import path
from .views import SignUp, AccountUserUpdate, set_me_author

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path("account/update/<int:pk>", AccountUserUpdate.as_view(), name='account_update'),
    path('account/setauthor/', set_me_author, name='set_me_author'),
]
