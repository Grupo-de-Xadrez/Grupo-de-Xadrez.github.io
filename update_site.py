import pathlib
import lichess.api

def main():
    projectFolder = pathlib.Path(__file__).parent.absolute()

    data = open(f'{projectFolder}/data.txt').read().split('\n')

    names = dict()
    abreviations = dict()
    nicknames = dict()
    rounds = list()
    playersSorted = (list(), list())
    ratings = (dict(), dict())

    analysing = None
    for line in data:
        if line.endswith(':'):
            analysing = line[:-1]
            if analysing == 'r':
                rounds.append(list())
            continue
        if analysing == 'n':
            if '=' in line:
                names[line.split('=')[0]] = line.split('=')[1]
            continue
        if analysing == 'a':
            if '=' in line:
                abreviations[line.split('=')[0]] = line.split('=')[1]
            continue
        if analysing == 'l':
            if '=' in line:
                nicknames[line.split('=')[0]] = line.split('=')[1]
            continue
        if analysing == 'r':
            if '=' in line:
                rounds[-1].append(((line.split('=')[0].split(',')[0], line.split('=')[0].split(',')[1]), (line.split('=')[1].split(',')[0], line.split('=')[1].split(',')[1])))

    lastRound = None
    currentRound = None
    nextRound = None

    for i, r in enumerate(rounds):
        if any(['' in g[1] for g in r]):
            currentRound = i
            if i > 0:
                lastRound = i-1
            if i < len(rounds) - 1:
                nextRound = i+1
            break
    else:
        lastRound = len(rounds) - 1

    def getName(cod):
        if names[cod] == '':
            return cod
        return names[cod]

    def getAbbreviation(cod):
        if abreviations[cod] == '':
            return cod
        return abreviations[cod]

    def toStrResult(game, ritmo):
        if game[1][ritmo] == 'w':
            return f'* **{getName(game[0][(ritmo + 0) % 2])}** *({ratings[ritmo][game[0][(ritmo + 0) % 2]]})* `1   -   0`  {getName(game[0][(ritmo + 1) % 2])} *({ratings[ritmo][game[0][(ritmo + 1) % 2]]})*'
        if game[1][ritmo] == 'd':
            return f'* {getName(game[0][(ritmo + 0) % 2])} *({ratings[ritmo][game[0][(ritmo + 0) % 2]]})* `1/2 - 1/2` {getName(game[0][(ritmo + 1) % 2])} *({ratings[ritmo][game[0][(ritmo + 1) % 2]]})*'
        if game[1][ritmo] == 'b':
            return f'* {getName(game[0][(ritmo + 0) % 2])} *({ratings[ritmo][game[0][(ritmo + 0) % 2]]})* `0   -   1` **{getName(game[0][(ritmo + 1) % 2])}** *({ratings[ritmo][game[0][(ritmo + 1) % 2]]})*'
        return f'* {getName(game[0][(ritmo + 0) % 2])} *({ratings[ritmo][game[0][(ritmo + 0) % 2]]})*     -     {getName(game[0][(ritmo + 1) % 2])} *({ratings[ritmo][game[0][(ritmo + 1) % 2]]})*'

    def toStrBye(r, ritmo):
        playersInBye = [f'{names[player]} ({ratings[ritmo][player]})' for player in names.keys() if not any(map(lambda g: g[0][0] == player, r)) and not any(map(lambda g: g[0][1] == player, r))]

        if len(playersInBye) == 0:
            return ''

        return '\n\n' + 'De folga: ' + ', '.join(playersInBye)

    def toStrRound(r, ritmo):
        return '\n'.join([toStrResult(g, ritmo) for g in r]) + toStrBye(r, ritmo)

    def toStrStandings(ritmo):
        points = {player: 0 for player in names.keys()}
        games = {player: 0 for player in names.keys()}
        gamesAsBlack = {player: 0 for player in names.keys()}
        wins = {player: 0 for player in names.keys()}

        for r in rounds:
            for g in r:
                if g[1][ritmo] == 'w':
                    points[g[0][0]] += 2
                    wins[g[0][0]] += 1
                elif g[1][ritmo] == 'd':
                    points[g[0][0]] += 1
                    points[g[0][1]] += 1
                elif g[1][ritmo] == 'b':
                    points[g[0][1]] += 2
                    wins[g[0][1]] += 1
                else:
                    continue
                games[g[0][0]] += 1
                games[g[0][1]] += 1
                gamesAsBlack[g[0][1]] += 1

        playersSorted[ritmo].extend(sorted(names.keys(), key = lambda player: (points[player], -games[player], gamesAsBlack[player], wins[player]), reverse=True))

        table = list(map(lambda player: (getName(player) + f' ({ratings[ritmo][player]})', points[player] / 2 if points[player] % 2 == 1 else points[player] // 2, games[player], gamesAsBlack[player], wins[player]), playersSorted[ritmo]))

        tableStr = ''

        tableStr += '| Pos | Nome | Pts | J | J P | V |'
        tableStr += '\n'
        tableStr += '| :---: | :--- | :---: | :---: | :---: | :---: |'

        lastI = None
        for i, entry in enumerate(table):
            tableStr += '\n'
            if i == 0 or entry[1:] != table[i - 1][1:]:
                tableStr += f'| {i + 1} | {" | ".join(map(str, entry))} |'
                lastI = i
            else:
                tableStr += f'| {lastI + 1} | {" | ".join(map(str, entry))} |'

        return tableStr

    def toStrCrossLine(cod, ritmo):
        lineStr = ''

        lineStr += f'| **{getAbbreviation(cod)}** '

        for player in playersSorted[ritmo]:
            if player == cod:
                lineStr += f'| :::::::: '
                continue

            result = '-'

            for r in rounds:
                for g in r:
                    if g[0][1] == cod and g[0][0] == player:
                        if g[1][ritmo] == 'w':
                            result = '0'
                        elif g[1][ritmo] == 'd':
                            result = '0.5'
                        elif g[1][ritmo] == 'b':
                            result = '1'
                        else:
                            result = ''

            # Feito duas vezes, para caso seja ida-volta, ele coloque na horizontal os resultados de brancas, senão (só ida), qualquer um.
            for r in rounds:
                for g in r:
                    if g[0][0] == cod and g[0][1] == player:
                        if g[1][ritmo] == 'w':
                            result = '1'
                        elif g[1][ritmo] == 'd':
                            result = '0.5'
                        elif g[1][ritmo] == 'b':
                            result = '0'
                        else:
                            result = ''

            lineStr += f'| {result} '

        lineStr += '|'

        return lineStr

    def toStrCrossTable(ritmo):
        tableStr = ''

        tableStr += '| | ' + ' | '.join([getAbbreviation(player) for player in playersSorted[ritmo]]) + ' |'
        tableStr += '\n'
        tableStr += '| :--- | ' + ' | '.join([':---:' for player in playersSorted[ritmo]]) + ' |'
        tableStr += '\n'
        tableStr += '\n'.join([toStrCrossLine(player, ritmo) for player in playersSorted[ritmo]])

        return tableStr

    def toStrParticipant(cod):
        return f'* {abreviations[cod]}: **{names[cod]}**, a.k.a. `[https://www.lichess.org/@/{nicknames[cod]}](@{nicknames[cod]})` *(Rapid: {ratings[0][cod]}, Blitz: {ratings[1][cod]})*'

    def toStrParticipants():
        return '\n'.join([toStrParticipant(cod) for cod in names.keys()])

    for cod in names.keys():
        perf = lichess.api.user(nicknames[cod])
        try:
            ratings[0][cod] = perf['perfs']['rapid']['rating']
        except:
            ratings[0][cod] = '-'
        try:
            ratings[1][cod] = perf['perfs']['blitz']['rating']
        except:
            ratings[1][cod] = '-'

    page = ''

    page += '## Participantes:'
    page += '\n'
    page += '\n'
    page += toStrParticipants()
    page += '\n'
    page += '\n'

    if currentRound != None:
        page += '### Rodada atual:'
        page += '\n'
        page += '\n'
        page += '#### Rapid:'
        page += '\n'
        page += '\n'
        page += toStrRound(rounds[currentRound], 0)
        page += '\n'
        page += '\n'
        page += '#### Blitz:'
        page += '\n'
        page += '\n'
        page += toStrRound(rounds[currentRound], 1)
        page += '\n'
        page += '\n'

    if lastRound != None:
        page += '### Rodada anterior:'
        page += '\n'
        page += '\n'
        page += '#### Rapid:'
        page += '\n'
        page += '\n'
        page += toStrRound(rounds[lastRound], 0)
        page += '\n'
        page += '\n'
        page += '#### Blitz:'
        page += '\n'
        page += '\n'
        page += toStrRound(rounds[lastRound], 1)
        page += '\n'
        page += '\n'

    if nextRound != None:
        page += '### Rodada seguinte:'
        page += '\n'
        page += '\n'
        page += '#### Rapid:'
        page += '\n'
        page += '\n'
        page += toStrRound(rounds[nextRound], 0)
        page += '\n'
        page += '\n'
        page += '#### Blitz:'
        page += '\n'
        page += '\n'
        page += toStrRound(rounds[nextRound], 1)
        page += '\n'
        page += '\n'

    page += '## Tabelas'
    page += '\n'
    page += '\n'

    page += '#### Rapid'
    page += '\n'
    page += '\n'
    page += toStrStandings(0)
    page += '\n'
    page += '\n'

    page += '#### Blitz'
    page += '\n'
    page += '\n'
    page += toStrStandings(1)
    page += '\n'
    page += '\n'

    page += '## Resultados'
    page += '\n'
    page += '\n'
    page += '#### Rapid:'
    page += '\n'
    page += '\n'
    page += toStrCrossTable(0)
    page += '\n'
    page += '\n'
    page += '#### Blitz:'
    page += '\n'
    page += '\n'
    page += toStrCrossTable(1)
    page += '\n'
    page += '\n'

    for i, r in enumerate(rounds):
        page += f'### Rodada {i + 1}:'
        page += '\n'
        page += '\n'
        page += '#### Rapid:'
        page += '\n'
        page += '\n'
        page += toStrRound(r, 0)
        page += '\n'
        page += '\n'
        page += '#### Blitz:'
        page += '\n'
        page += '\n'
        page += toStrRound(r, 1)
        page += '\n'
        page += '\n'

    open(f'{projectFolder}/index.md', 'w').write(page)

if __name__ == '__main__':
    main()
