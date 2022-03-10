from os import name

from discord import player


class Carte_mystere:
    def __init__(self, label, points):
        self.label = label
        self.points = points

    def __str__(self):
        return 'Cartes mystere :\nlabel : %s\npoints : %i' % (self.label, self.points)

class Carte_puriste:
    def __init__(self, label, answer, points):
        self.label = label
        self.answer = answer
        self.points = points

    def __str__(self):
        return 'Cartes puristes :\nlabel : %s\nanswer : %s\npoints : %i' % (self.label, self.answer, self.points)


class Team:
    def __init__(self, name):
        self.name = name
        self.players = list()
        self.score = 0
        self.current = False

    def is_player_in_team(self, player):
        return any(player in p for p in self.players)

    def __str__(self):
        return 'EQUIPE %s\nSCORES : %s\nJOUEURS :\n%s' % (self.name, self.score, self.players)