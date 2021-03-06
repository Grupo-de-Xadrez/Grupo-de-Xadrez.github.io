class PlayerStats:
    def __init__(self):
        self.wins_as_white = []
        self.loses_as_white = []
        self.ties_as_white = []
        self.wins_as_black = []
        self.loses_as_black = []
        self.ties_as_black = []
        self.relative_position = 1


    @property
    def number_of_wins_as_white(self):
        return len(self.wins_as_white)

    @property
    def number_of_loses_as_white(self):
        return len(self.loses_as_white)

    @property
    def number_of_ties_as_white(self):
        return len(self.ties_as_white)

    @property
    def number_of_wins_as_black(self):
        return len(self.wins_as_black)

    @property
    def number_of_loses_as_black(self):
        return len(self.loses_as_black)

    @property
    def number_of_ties_as_black(self):
        return len(self.ties_as_black)

    @property
    def number_of_wins(self):
        return self.number_of_wins_as_white + self.number_of_wins_as_black

    @property
    def number_of_loses(self):
        return self.number_of_loses_as_white + self.number_of_loses_as_black

    @property
    def number_of_ties(self):
        return self.number_of_ties_as_white + self.number_of_ties_as_black

    @property
    def points(self):
        return self.number_of_wins + self.number_of_ties / 2.0

    @property
    def number_of_games(self):
        return self.number_of_wins + self.number_of_loses + self.number_of_ties

    @property
    def number_of_games_as_white(self):
        return self.number_of_wins_as_white + self.number_of_loses_as_white + self.number_of_ties_as_white

    @property
    def number_of_games_as_black(self):
        return self.number_of_wins_as_black + self.number_of_loses_as_black + self.number_of_ties_as_black

    def better_than(self, player_stats):
        if self.points != player_stats.points:
            return self.points > player_stats.points
        elif self.number_of_games != player_stats.number_of_games:
            return self.number_of_games < player_stats.number_of_games
        elif self.number_of_games_as_black != player_stats.number_of_games_as_black:
            return self.number_of_games_as_black > player_stats.number_of_games_as_black
        elif self.number_of_wins != player_stats.number_of_wins:
            return self.number_of_wins > player_stats.number_of_wins
        else:
            return False

    def get_result_as_white_versus(self, player):
        if any([game.black_player == player for game in self.wins_as_white]):
            return 1.0
        elif any([game.black_player == player for game in self.loses_as_white]):
            return 0.0
        elif any([game.black_player == player for game in self.ties_as_white]):
            return 0.5
        else:
            return None

    def get_result_as_black_versus(self, player):
        if any([game.white_player == player for game in self.wins_as_black]):
            return 1.0
        elif any([game.white_player == player for game in self.loses_as_black]):
            return 0.0
        elif any([game.white_player == player for game in self.ties_as_black]):
            return 0.5
        else:
            return None