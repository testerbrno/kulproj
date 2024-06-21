from django.urls import path
from django.views.generic import ListView, CreateView, DetailView
from tournaments.models import Tournament, Match
from tournaments.views import *
# from tournaments.views import TournamentDetailView, RoundDetailView, TournamentCreateView, TournamentUpdateView, MatchPlayerCreateView, MatchPlayerUpdateView, AddFormView, DeleteFormView

urlpatterns = [
    path('', TournamentListView.as_view(template_name="./tournament/tournament_list.html"), name='tournament_list'),
    path('<int:tournament_pk>/round/', RoundListView.as_view(template_name="./tournament/round_list.html"), name='round_list'),
    path('<int:tournament_pk>/<int:round_pk>/match/', MatchListView.as_view(template_name="./tournament/match_list.html"), name='match_list'),
    path('<int:tournament_pk>/', TournamentDetailView.as_view(template_name="./tournament/tournament_detail.html"), name='tournament_detail'),
    path('<int:tournament_pk>/<int:round_pk>/', RoundDetailView.as_view(template_name="./tournament/round_detail.html"), name='round_detail'),

    # URL patterns for creating and updating tournaments
    path('create/',TournamentCreateView.as_view(template_name="./form.html"), name='tournament_create'),
    path('<int:tournament_pk>/update/', TournamentUpdateView.as_view(template_name="./tournament/tournament_create.html"), name='tournament_update'),

    # URL patterns for creating and updating rounds
    path('<int:tournament_pk>/round/create/', RoundCreateView.as_view(template_name="./form.html"), name='round_create'),
    # path('<int:tournament_pk>/<int:round_pk>/update/', RoundUpdateView.as_view(template_name="./update/round_update.html"), name='round_update'),
    path('<int:tournament_pk>/<int:round_pk>/match/create/', MatchCreateView.as_view(template_name="./form.html"), name='match_create'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/', MatchDetailView.as_view(template_name="./tournament/match_detail.html"), name='match_detail'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/update/', MatchUpdateView.as_view(template_name="./form.html"), name='match_update'),
    path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/playerscore/create/', PlayerScoreCreateView.as_view(template_name="./tournament/playerscore.html"), name='playerscore_create'),
    # path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/<str:form_class>/create/', MatchPlayerCreateView.as_view(template_name="./create/match_player_form.html"), name='matchplayer_create'),
    # path('<int:tournament_pk>/<int:round_pk>/<int:match_pk>/<int:matchplayer_pk>/update/', MatchPlayerUpdateView.as_view(template_name='./update/match_player_update.html'), name='matchplayer_update'),

    # URL pattern for adding formsets using HTMX
    # path('<str:form_class>/add_form/', AddFormView.as_view(), name='add_form'),
    path('delete_form/', DeleteFormView.as_view(), name='delete_form'),
    # path('<str:form_class>/add_update_form/', AddFormView.as_view(), name='add_update_form'),
]