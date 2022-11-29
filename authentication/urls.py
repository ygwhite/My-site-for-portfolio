from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('registration/', views.RegisterView.as_view(), name='registration'),
    path('logout/', views.logout_user, name='logout')
]