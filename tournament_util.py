import pandas as pd
from datetime import date
import random


class Player:
    def __init__(self, name):
        self.name = name


class Team:
    def __init__(self, teamname, playera: Player = None, playerb: Player = None, courts=0):
        self.name = teamname
        self.playera: Player = playera
        self.playerb: Player = playerb
        self.courts=0

    def __str__(self):
        return f"{self.name}: {self.playera} & {self.playerb}"

    def set_players(self, playera: Player, playerb: Player):
        self.playera = playera
        self.playerb = playerb

    def set_playera(self, playera: Player):
        self.playera = playera

    def set_playerb(self, playerb: Player):
        self.playerb = playerb
    
    def set_court(self, courts):
        self.courts = courts
    

class Match:
    def __init__(self, teama: Team, teamb: Team):
        self.teama: Team = teama
        self.teamb: Team = teamb
        

class Tournament:
    recommended_teams = 8
    recommended_courts = 4
    min_teams = 6
    min_courts = 2

    def __init__(self, tournament_name: str, creation_date: date=None):
        self.name = tournament_name
        self.teams = []
        self.ranking = []
        self.courts = 0
        self.mode = None
        self.creation_date = creation_date if creation_date is not None else date.today()

    def register_team(self, team: Team):
        self.teams.append(team)
        self.courts += team.courts

    def __str__(self):
        return f"{self.name} [{self.mode} mode]: {self.creation_date}"
    

    def status_code(self):
        # -1: not possible
        if len(self.teams) < self.min_teams or self.courts < self.min_courts:
            return -1
        # 0: possible, but not recommended
        elif len(self.teams) < self.recommended_teams or self.courts < self.recommended_courts:
            return 0
        # 1: possible
        else:
            return 1


class SwissTournament(Tournament):
    def __init__(self, tournament_name: str):
        super().__init__(tournament_name)
        self.mode = "Swiss"
        self.ladder = []

    def initialize_ranking(self):
        self.ranking = random.sample(self.teams)


if __name__ == "__main__":
    st = SwissTournament("First Try")
    pass