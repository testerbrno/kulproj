from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, View
from django.urls import reverse_lazy, reverse
from tournaments.models import *
from tournaments.forms import *

class ContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check for tournament_pk in URL parameters
        if 'tournament_pk' in self.kwargs:
            self.tournament_instance = get_object_or_404(Tournament, pk=self.kwargs.get('tournament_pk'))
            context['tournament'] = self.tournament_instance
            context['rounds'] = self.tournament_instance.rounds.all()
            context['organizers'] = self.tournament_instance.organizers.all()
            context['players'] = self.tournament_instance.players.all()

        # Check for round_pk in URL parameters
        if 'round_pk' in self.kwargs:
            self.round_instance = get_object_or_404(Round, pk=self.kwargs.get('round_pk'))
            context['round'] = self.round_instance
            context['matches'] = self.round_instance.matches.all()

        # Check for match_pk in URL parameters
        if 'match_pk' in self.kwargs:
            self.match_instance = get_object_or_404(Match, pk=self.kwargs.get('match_pk'))
            context['match'] = self.match_instance
            context['playerscores'] = self.match_instance.match_players.all()

        # Check for playerscore_pk in URL parameters
        if 'playerscore_pk' in self.kwargs:
            self.playerscore_instance = get_object_or_404(PlayerScore, pk=self.kwargs.get('playerscore_pk'))
            context['playerscore'] = self.playerscore_instance
        
        return context

class DeleteFormView(TemplateView):
    def delete(self, request, *args, **kwargs):
        return HttpResponse()

class TournamentCreateView(ContextMixin, CreateView):
    model = Tournament
    form_class = TournamentForm

    def get_success_url(self):
        return reverse('round_create', kwargs={'tournament_pk': self.object.pk})

class TournamentDetailView(ContextMixin, DetailView):
    model = Tournament
    context_object_name = 'tournament'

    def get_object(self):
        return Tournament.objects.get(pk=self.kwargs['tournament_pk'])

class TournamentUpdateView(ContextMixin, UpdateView):
    model = Tournament
    form_class = TournamentForm
    
    def get_object(self):
        return Tournament.objects.get(pk=self.kwargs['tournament_pk'])

    def get_success_url(self):
        return reverse('tournament_update', kwargs={'tournament_pk': self.object.pk})

class RoundCreateView(ContextMixin, CreateView):
    model = Round
    form_class = RoundForm
    
    def get_initial(self):
        tournament_from_url = self.kwargs.get('tournament_pk')
        return {
            'tournament': tournament_from_url,
            }

    def form_valid(self, form):
        form.instance.tournament = get_object_or_404(Tournament, pk=self.kwargs.get('tournament_pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tournament_detail', kwargs={'tournament_pk': self.object.tournament.pk})

class RoundDetailView(ContextMixin, DetailView):
    model = Round
    context_object_name = 'round'

    def get_object(self):
        return Round.objects.get(pk=self.kwargs['round_pk'])

class MatchCreateView(ContextMixin, CreateView):
    model = Match
    form_class = MatchForm

    def get_initial(self):
        round_from_url = self.kwargs.get('round_pk')
        return {
            'round': round_from_url,
            }

    def form_valid(self, form):
        form.instance.round = get_object_or_404(Round, pk=self.kwargs.get('round_pk'))
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse('playerscore_create', kwargs={
            'tournament_pk': self.object.round.tournament.pk,
            'round_pk': self.object.round.pk,
            'match_pk': self.object.pk
        })

class RoundUpdateView(UpdateView):
    model = Round
    form_class = RoundForm

    def get_object(self):
        return Round.objects.get(pk=self.kwargs['round_pk'])

    def form_valid(self, form):
        form.instance.tournament = get_object_or_404(Tournament, pk=self.kwargs.get('tournament_pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('roundmatch_update', kwargs={
            'tournament_pk': self.object.tournament.pk,
            'round_pk': self.object.pk
        })

class MatchDetailView(ContextMixin, DetailView):
    model = Match
    context_object_name = 'match'

    def get_object(self):
        return Match.objects.get(pk=self.kwargs['match_pk'])

class MatchUpdateView(ContextMixin, UpdateView):
    model = Match
    form_class = MatchForm

    def get_object(self):
        return get_object_or_404(Match, pk=self.kwargs['match_pk'])

    def get_success_url(self):
        return reverse('match_update', kwargs={
            'tournament_pk': self.object.round.tournament.pk,
            'round_pk': self.object.round.pk,
            'match_pk': self.object.pk
        })

class MatchListView(ContextMixin, ListView):
    model = Match
    context_object_name = 'matches'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if 'tournament_pk' in self.kwargs:
            queryset = queryset.filter(round__tournament__pk=self.kwargs.get('tournament_pk'))

        if 'round_pk' in self.kwargs:
            queryset = queryset.filter(round__pk=self.kwargs.get('round_pk'))
        
        return queryset

class TournamentListView(ListView):
    model = Tournament
    context_object_name = 'tournaments'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset

class RoundListView(ContextMixin, ListView):
    model = Round
    context_object_name = 'rounds'

class PlayerScoreCreateView(ContextMixin, CreateView):
    model = PlayerScore
    form_class = PlayerScoreForm

    def dispatch(self, request, *args, **kwargs):
        match_pk = self.kwargs.get('match_pk')
        playerscore_count = PlayerScore.objects.filter(match_id=match_pk).count()
        
        if playerscore_count >= 2:
            return HttpResponseRedirect(reverse('playerscore_update', kwargs={
                'tournament_pk': self.kwargs['tournament_pk'],
                'round_pk': self.kwargs['round_pk'],
                'match_pk': match_pk
            }))
        
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        match_pk = self.kwargs.get('match_pk')
        initial['match'] = get_object_or_404(Match, pk=match_pk)
        return initial

    def form_valid(self, form):
        match = form.cleaned_data['match']
        player = form.cleaned_data['player']
        round = match.round

        existing_scores = PlayerScore.objects.filter(match__round=round, player=player)
        if existing_scores.exists():
            form.add_error('player', 'This player is already assigned to another match in this round.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        match = self.object.match
        playerscore_count = PlayerScore.objects.filter(match=match).count()
        
        if playerscore_count >= 2:
            return reverse('match_list', kwargs={
                'tournament_pk': match.round.tournament.pk,
                'round_pk': match.round.pk,
            })
        else:
            return reverse('playerscore_create', kwargs={
                'tournament_pk': match.round.tournament.pk,
                'round_pk': match.round.pk,
                'match_pk': match.pk
            })

class PlayerScoreUpdateView(ContextMixin, UpdateView):
    model = PlayerScore
    form_class = PlayerScoreForm

    def dispatch(self, request, *args, **kwargs):
        match_pk = self.kwargs.get('match_pk')
        self.playerscores = PlayerScore.objects.filter(match_id=match_pk)
        playerscore_count = self.playerscores.count()
        
        if playerscore_count < 2:
            return HttpResponseRedirect(reverse('playerscore_create', kwargs={
                'tournament_pk': self.kwargs['tournament_pk'],
                'round_pk': self.kwargs['round_pk'],
                'match_pk': match_pk
            }))
        
        # Initialize counter in session if not set
        if 'counter' not in request.session:
            request.session['counter'] = 0

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        counter = self.request.session['counter']
        if counter == 0:
            return self.playerscores.first()
        elif counter == 1:
            return self.playerscores.last()
        return super().get_object(queryset)

    def get_initial(self):
        initial = super().get_initial()
        initial['match'] = self.object.match
        return initial

    def form_valid(self, form):
        match = form.cleaned_data['match']
        player = form.cleaned_data['player']
        round = match.round

        existing_scores = PlayerScore.objects.filter(match__round=round, player=player).exclude(pk=self.object.pk)
        if existing_scores.exists():
            form.add_error('player', 'This player is already assigned to another match in this round.')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        
        if self.request.session['counter'] == 0:
            self.request.session['counter'] = 1
            return HttpResponseRedirect(self.get_success_url())

        # Reset counter after the second player is updated
        self.request.session['counter'] = 0
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        match = self.object.match
        if self.request.session['counter'] == 1:
            return reverse('playerscore_update', kwargs={
                'tournament_pk': match.round.tournament.pk,
                'round_pk': match.round.pk,
                'match_pk': match.pk
            })
        else:
            return reverse('match_list', kwargs={
                'tournament_pk': match.round.tournament.pk,
                'round_pk': match.round.pk
            })

class RoundMatchUpdateView(ContextMixin, TemplateView):
    template_name = "tournament/round_update_match_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_update_view = RoundUpdateView.as_view()(self.request, **kwargs)
        match_list_view = MatchListView.as_view()(self.request, **kwargs)
        
        context['round_update_form'] = round_update_view.context_data['form']
        context['matches'] = match_list_view.context_data['matches']
        return context