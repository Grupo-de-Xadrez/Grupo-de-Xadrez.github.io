from round import Round

class Tournament:
    def __init__(self, ritmo, data, index, players, cache):
        self.__ritmo = ritmo
        self.__players = players
        self.__rounds = []

        round_data = None
        for line in data:
            if line.startswith('\t'):
                pass
            elif line.endswith(':'):
                analysing = line[:-1]
                if analysing == 'r':
                    if round_data != None:
                        self.__rounds.append(Round(round_data, ritmo, index, players, cache))
                    round_data = []
            elif analysing == 'r' and '=' in line:
                if round_data != None:
                    round_data.append(line)
        if round_data != None:
            self.__rounds.append(Round(round_data, ritmo, index, players, cache))

    def compute_stats(self):
        for player in self.__players:
            player.init_stats(self.__ritmo)

        for round in self.__rounds:
            round.compute_stats()

        for player_1 in self.__players:
            for player_2 in self.__players:
                if player_1.better_than(player_2, self.__ritmo):
                    player_2.stats(self.__ritmo).relative_position += 1

        self.__players = list(sorted(self.__players, key=lambda player: player.stats(self.__ritmo).relative_position))

    @property
    def rounds(self):
        return self.__rounds # Allows extern modification

    def table(self):
        table = ''

        table += '| Pos | Nome | Pts | J | J P | V |'
        table += '\n'

        table += '| :---: | :--- | :---: | :---: | :---: | :---: |'
        table += '\n'

        table += '\n'.join(map(lambda player: player.table_entry(self.__ritmo), self.__players))

        return table

    def cross_table(self):
        cross_table = ''

        cross_table += '| | ' + ' | '.join([player.abbreviation for player in self.__players]) + ' |'
        cross_table += '\n'

        cross_table += '| :--- | ' + ' | '.join([':---:' for _ in self.__players]) + ' |'
        cross_table += '\n'

        cross_table += '\n'.join([player.cross_table_entry(self.__ritmo, self.__players) for player in self.__players]) # Allows intern modification

        return cross_table