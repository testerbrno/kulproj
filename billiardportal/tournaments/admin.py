from django.contrib import admin
from .models import Tournament, Round, Match, PlayerScore

admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Match)
admin.site.register(PlayerScore)
