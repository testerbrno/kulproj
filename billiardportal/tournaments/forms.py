from django import forms
from tournaments.models import (
    Tournament,
    Round,
    Match,
    PlayerScore
)

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

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['round']

class PlayerScoreForm(forms.ModelForm):
    class Meta:
        model = PlayerScore
        fields = ['match', 'player', 'score']
