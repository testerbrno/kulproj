from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .models import Player
from .views import PlayerSearchView, PlayerCreateView, PlayerUpdateView

urlpatterns = [
    path('', ListView.as_view(model=Player, template_name="./player/player_list.html"), name='player_list'),
    path('<int:pk>/', DetailView.as_view(model=Player, template_name="./player/player_detail.html"), name='player_detail'),
    # path('search/', PlayerSearchView.as_view(), name='player_search'),
    path('register/', PlayerCreateView.as_view(model=Player, template_name="./player/user_registration.html"), name='player_create'),
    path('<int:pk>/update/', PlayerUpdateView.as_view(model=Player, template_name="./player/player_update.html"), name='player_update'),
    # path('password_change/', PasswordChangeView.as_view(template_name="./change_password.html"), name='password_change'),
    # path('password_change/done/', PasswordChangeDoneView.as_view(template_name="./change_password_done.html"), name='password_change_done'),
]