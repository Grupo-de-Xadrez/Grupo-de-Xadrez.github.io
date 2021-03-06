from game import Game

class Round:
    def __init__(self, round_data, ritmo, index, players, cache):
        self.__ritmo = ritmo
        self.__games = []
        self.__byes_long_names = list(map(lambda player: player.long_name(ritmo), players))

        for line in round_data:
            for player in players:
                if player.code == line.split('=')[0].split(',')[0]:
                    player_1 = player
                elif player.code == line.split('=')[0].split(',')[1]:
                    player_2 = player

            if index % 2 == 0:
                self.__games.append(Game(ritmo, player_1, player_2, line.split('=')[1].split(',')[index], cache))
            else:
                self.__games.append(Game(ritmo, player_2, player_1, line.split('=')[1].split(',')[index], cache))

            self.__byes_long_names.remove(player_1.long_name(ritmo))
            self.__byes_long_names.remove(player_2.long_name(ritmo))

    @property
    def closed(self):
        return all([game.closed for game in self.__games])

    def compute_stats(self):
        for game in self.__games:
            game.compute_stats()

    def __str__(self):
        return '\n'.join(map(str, self.__games)) + '\n\n' + 'De folga: ' + ', '.join(self.__byes_long_names)
