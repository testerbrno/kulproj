from django.db import models
from core.models import Player

class Tournament(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    organizers = models.ManyToManyField(Player, related_name='organized_tournaments')
    players = models.ManyToManyField(Player, related_name='participating_tournaments')

    def __str__(self):
        return self.name

class Round(models.Model):
    name = models.CharField(max_length=255)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    tournament = models.ForeignKey(Tournament, related_name='rounds', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.tournament.name}"

class Match(models.Model):
    round = models.ForeignKey(Round, related_name='matches', on_delete=models.CASCADE)
    referee = models.ManyToManyField(Player, related_name='refereed_matches')

    def __str__(self):
        return f"Match in {self.round.name}"

class PlayerScore(models.Model):
    match = models.ForeignKey(Match, related_name='match_players', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='player_matches', on_delete=models.CASCADE)
    score = models.IntegerField(default=0, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'player'], name='unique_match_player')
        ]

    def __str__(self):
        return f"{self.player.username} in {self.match} with score {self.score}"
