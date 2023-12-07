import pandas as pd
from datetime import date
import random
from abc import ABC, abstractmethod
from faker import Faker
from faker.providers import emoji
import uuid

class Player:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Team:
    def __init__(
        self, teamname, playera: Player = None, playerb: Player = None, courts=0
    ):
        self.name = teamname
        self.playera: Player = playera
        self.playerb: Player = playerb
        self.courts = 0

    def __str__(self):
        return f"{self.name}: {str(self.playera)} & {str(self.playerb)}"

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
    __match_codes = set()
    winning_points = 15
    sets = 2
    def __init__(self, teama: Team, teamb: Team):
        self.teama: Team = teama
        self.teamb: Team = teamb
        self.is_over = False
        
        self.match_code = Match.create_match_id()
        print(self.match_code)

    def create_match_id():
        i = 0
        while i <= 100:
            match_code = str(uuid.uuid4())[:3]
            if not match_code in Match.__match_codes:
                Match.__match_codes.add(match_code)
                return match_code
        if i >= 100:
            raise Exception("Match ID Bug fml")

    def __str__(self):
        return f"{str(self.teama)} vs {str(self.teamb)}"
    
    def submit_results(self, results: list[tuple[2]]):
        self.results = results
        self.is_over = True

    def get_winner(self) -> Team:
        if self.is_over:
            return None
        else:
            gamesa, gamesb, pointsa, pointsb = self.evaluate_results(self.results)
            if gamesa > gamesb:
                return self.teama
            elif gamesa < gamesb:
                return self.teamb
            elif gamesa == gamesb and pointsa > pointsb:
                return self.teama
            elif gamesa == gamesb and pointsa < pointsb:
                return self.teamb
            else:
                # TODO how to handle draw?
                return self.teama
    
    def evaluate_results(self, results):
            gamesa = 0
            gamesb = 0
            pointsa = 0
            pointsb = 0
            for scorea, scoreb in self.results:
                pointsa += scorea
                pointsb += scoreb
                if scorea > scoreb:
                    gamesa += 1
                else:
                    gamesb +=1
            return gamesa, gamesb, pointsa, pointsb
    
    def get_names(self):
        return [self.teama.playera.name, self.teama.playerb.name, self.teamb.playera.name, self.teamb.playerb.name]

    def has_player(self, name):
        return name in self.get_names()



class Round:
    def __init__(self, teams: list[Team]):
        self.teams: list[Team] = teams
        self.matches: list[Match] = []

    @abstractmethod
    def initializeMatches(self):
        pass

    def get_match(self, match_code=None, name=None):
        return next((match for match in self.matches if match.match_code == match_code or match.has_player(name)), None)


class Tournament:
    min_teams = 6
    min_courts = 2

    def __init__(self, tournament_name: str, creation_date: date = None):
        self.name = tournament_name
        self.teams = []
        self.ranking = []
        self.rounds = []
        self.courts = 0
        self.mode = None
        self.creation_date = (
            creation_date if creation_date is not None else date.today()
        )
        self.current_round = 0


    def register_team(self, team: Team):
        self.teams.append(team)
        self.courts += team.courts

    def __str__(self):
        return f"{self.name} [{self.mode} mode]: {self.creation_date}"

    def status_code(self):
        # -1: not possible
        if len(self.teams) < self.min_teams or self.courts < self.min_courts:
            return -1
        else:
            return self.current_round
    
    @abstractmethod
    def initializeRound(self, current_round: int):
        pass
    
    def get_match(self, match_code:str=None, name:str=None)-> Match:
        return self.rounds[self.current_round - 1].get_match(match_code=match_code, name=name)
    
    def submit_results(self, results: list[tuple[2]], name:str=None, match_code:str=None)->bool:
        match = self.get_match(name=name, match_code=match_code)
        if match is None:
            # TODO exception hier?
            return False
        match.submit_results(results)




class SwissTournament(Tournament):
    def __init__(self, tournament_name: str):
        super().__init__(tournament_name)
        self.mode = "Swiss"

    def initializeRound(self, current_round: int):
        if current_round == 0:
            # first round
            # initialize with random seeding
            sr = SwissRound(self.teams)
            sr.initializeMatches(SwissRound.randomSeeding(sr.teams))
            self.rounds.append(sr)
        
        self.current_round += 1


class SwissRound(Round):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)

    def initializeMatches(self, seeding_teams: list[Team]):
        if len(seeding_teams) % 2 != 0:
            seeding_teams.append(None)
        self.matches: list[Match] = [
            Match(seeding_teams[i], seeding_teams[i + 1])
            for i in range(0, len(seeding_teams), 2)
        ]
    
    def randomSeeding(teams: list[Team]) -> list[Team]:
        return random.sample(teams, len(teams))


if __name__ == "__main__":
    st = SwissTournament("First Try")
    fake = Faker()
    fake.add_provider(emoji)

    for _ in range(8):
        team = Team(fake.emoji(), Player(fake.name()), Player(fake.name()))
        # print(team)
        st.register_team(team)

    st.initializeRound(st.current_round)
    pass
    match = st.get_match(name=team.playera.name)
    pass