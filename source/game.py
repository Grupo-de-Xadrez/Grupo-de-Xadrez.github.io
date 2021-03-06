import lichess.api
from result import Result

class Game:
    def __init__(self, ritmo, white_player, black_player, result_or_code, cache):
        self.__ritmo = ritmo
        self.__white_player = white_player
        self.__black_player = black_player

        if result_or_code == '':
            self.__result = Result.NOT_YET_PLAYED
        elif result_or_code == 'w':
            self.__result = Result.WHITE_WON
        elif result_or_code == 'b':
            self.__result = Result.BLACK_WON
        elif result_or_code == 'd':
            self.__result = Result.DRAW
        else:
            self.__code = result_or_code
            self.__link = f'https://www.lichess.org/{self.__code}'
            self.__data = cache.get(self.__code, None) or lichess.api.game(self.__code)
            cache[self.__code] = self.__data

            self.__result = Result.parse(self.__data.get('winner', None))
            self.__opening = f'{self.__data["opening"]["eco"]} - {self.__data["opening"]["name"]}'

            if self.__data.get('players', {}).get('white', {}).get('user', {}).get('name', None) == black_player.nickname and self.__data.get('players', {}).get('black', {}).get('user', {}).get('name', None) == white_player.nickname:
                self.__warning = 'INVERTIDO'
                self.__result = Result.reverse(self.__result)

    @property
    def white_player(self):
        return self.__white_player # Allows extern modification

    @property
    def black_player(self):
        return self.__black_player # Allows extern modification

    @property
    def link(self):
        return self.__link

    @property
    def opening(self):
        return self.__opening

    @property
    def closed(self):
        return self.__result != Result.NOT_YET_PLAYED

    def compute_stats(self):
        if self.__result == Result.WHITE_WON:
            self.__white_player.stats(self.__ritmo).wins_as_white.append(self)
            self.__black_player.stats(self.__ritmo).loses_as_black.append(self)
        elif self.__result == Result.BLACK_WON:
            self.__white_player.stats(self.__ritmo).loses_as_white.append(self)
            self.__black_player.stats(self.__ritmo).wins_as_black.append(self)
        elif self.__result == Result.DRAW:
            self.__white_player.stats(self.__ritmo).ties_as_white.append(self)
            self.__black_player.stats(self.__ritmo).ties_as_black.append(self)

    def __str__(self):
        return self.header() + ' ' + self.warning_header() + '\n\n' + '**>**' + ' ' + self.body()

    def header(self):
        if  self.__result == Result.NOT_YET_PLAYED:
            return f'* {self.__white_player.long_name(self.__ritmo)} `\u00b7 - \u00b7` {self.__black_player.long_name(self.__ritmo)}'
        elif self.__result == Result.WHITE_WON:
            return f'* **{self.__white_player.long_name(self.__ritmo)}** `1   -   0` {self.__black_player.long_name(self.__ritmo)}'
        elif self.__result == Result.BLACK_WON:
            return f'* {self.__white_player.long_name(self.__ritmo)} `0   -   1` **{self.__black_player.long_name(self.__ritmo)}**'
        elif self.__result == Result.DRAW:
            return f'* {self.__white_player.long_name(self.__ritmo)} `\u00bd - \u00bd` {self.__black_player.long_name(self.__ritmo)}'

    def warning_header(self):
        try:
            return f'`{self.__warning}`'
        except AttributeError:
            return ''

    def body(self):
        try:
            return f'[\u2197]({self.link})'
        except AttributeError:
            return ''
