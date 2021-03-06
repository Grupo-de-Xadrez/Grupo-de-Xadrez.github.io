import lichess.api
from player_stats import PlayerStats

class Player:
    def __init__(self, code, data):
        self.__code = code
        self.__stats = {}

        for line in data:
            if line.startswith('\t'):
                pass
            elif line.endswith(':'):
                analysing = line[:-1]
            elif '=' in line and line.split('=')[0] == self.__code:
                if analysing == 'n':
                    self.__name = line.split('=')[1]
                elif analysing == 'a':
                    self.__abbreviation = line.split('=')[1]
                elif analysing == 'l':
                    self.__nickname = line.split('=')[1]
                    self.__perf = lichess.api.user(self.__nickname)

    def update(self):
        self.__perf = lichess.api.user(self.__nickname)

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @property
    def abbreviation(self):
        return self.__abbreviation

    @property
    def nickname(self):
        return self.__nickname

    @property
    def link(self):
        return f'https://www.lichess.org/@/{self.nickname}'

    def __eq__(self, player):
        return self.code == player.code

    def rating(self, ritmo):
        return self.__perf['perfs'][ritmo]['rating']

    def resume(self, ritmos):
        return f'{self.abbreviation}: **{self.name}**, a.k.a. [@{self.nickname}]({self.link}) ({", ".join([f"{ritmo}: {self.rating(ritmo)}" for ritmo in ritmos])})'

    def long_name(self, ritmo):
        return f'{self.name} *({self.rating(ritmo)})*'

    def stats(self, ritmo):
        return self.__stats[ritmo] # Allows extern modification

    def init_stats(self, ritmo):
        self.__stats[ritmo] = PlayerStats()

    def better_than(self, player, ritmo):
        return self.stats(ritmo).better_than(player.stats(ritmo))

    def table_entry(self, ritmo):
        return f'| {self.stats(ritmo).relative_position} | {self.long_name(ritmo)} | {self.stats(ritmo).points} | {self.stats(ritmo).number_of_games} | {self.stats(ritmo).number_of_games_as_black} | {self.stats(ritmo).number_of_wins} |'

    def cross_table_entry(self, ritmo, players):
        table_entry = f'| **{self.abbreviation}** |'

        for player in players:
            table_entry += ' '
            if self == player:
                table_entry += '::::::::'
            else:
                result_as_white_versus_player = self.stats(ritmo).get_result_as_white_versus(player)
                if result_as_white_versus_player == 1.0:
                    table_entry += '1'
                elif result_as_white_versus_player == 0.0:
                    table_entry += '0'
                elif result_as_white_versus_player == 0.5:
                    table_entry += '\u00bd'
                else:
                    table_entry += ''
            table_entry += ' |'

        return table_entry
