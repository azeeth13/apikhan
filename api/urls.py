from django.urls import path,include
from .views import UserSignUp1
from .views import DeleteAccountView


urlpatterns = [
    path('userapi/',UserSignUp1.as_view()),
    path('rest-auth/delete-account/<str:username>/',DeleteAccountView.as_view(),name='delete-account')
]
