from django.urls import path
from .views import current_user, UserList, RegistrationAPIView, login

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('register/', RegistrationAPIView.as_view()),
    path('login/', login, name='api_login'),
]
