from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from tournaments.models import Tournament
from tournaments.forms import TournamentForm

class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    success_url = reverse_lazy('tournaments')

    # def get_success_url(self):
    #     return reverse('tournament_detail', kwargs={'tournament_pk': self.object.pk})

class TournamentDetailView(DetailView):
    model = Tournament
    context_object_name = 'tournament'

    def get_object(self):
        return Tournament.objects.get(pk=self.kwargs['tournament_pk'])

class TournamentUpdateView(UpdateView):
    model = Tournament
    form_class = TournamentForm
    
    def get_object(self):
        return Tournament.objects.get(pk=self.kwargs['tournament_pk'])

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'tournament_pk': self.object.pk})