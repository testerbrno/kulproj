from django import forms
from django.forms import inlineformset_factory
from tournaments.models import *

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'start_date', 'end_date', 'attachment', 'organizers', 'players']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ['name', 'attachment', 'tournament']
        widgets = {
            'tournament': forms.Select(attrs={'readonly': 'readonly'}),
        }

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['round', 'referee']
        widgets = {
            'round': forms.Select(attrs={'readonly': 'readonly'}),
        }

class PlayerScoreForm(forms.ModelForm):
    class Meta:
        model = PlayerScore
        fields = ['match', 'player', 'score']
        widgets = {
            'match': forms.Select(attrs={'readonly': 'readonly'}),
        }

