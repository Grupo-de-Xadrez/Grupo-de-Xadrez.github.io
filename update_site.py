data = open('data.txt').read().split('\n')

names = dict()
abreviations = dict()
rounds = list()
playersSorted = list()

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
    if analysing == 'r':
        if '=' in line:
            rounds[-1].append(((line.split('=')[0].split(',')[0], line.split('=')[0].split(',')[1]), line.split('=')[1]))

lastRound = None
currentRound = None
nextRound = None

for i, r in enumerate(rounds):
    if any([g[1] == '' for g in r]):
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

def toStrResult(game):
    if game[1] == 'w':
        return f'* **{getName(game[0][0])}**  `1   -   0`  {getName(game[0][1])}'
    if game[1] == 'd':
        return f'* {getName(game[0][0])} `1/2 - 1/2` {getName(game[0][1])}'
    if game[1] == 'b':
        return f'* {getName(game[0][0])} `0   -   1` **{getName(game[0][1])}**'
    return f'* {getName(game[0][0])}     -     {getName(game[0][1])}'

def toStrBye(r):
    playersInBye = [names[player] for player in names.keys() if not any(map(lambda g: g[0][0] == player, r)) and not any(map(lambda g: g[0][1] == player, r))]

    if len(playersInBye) == 0:
        return ''

    return '\n\n' + 'De folga: ' + ', '.join(playersInBye)


def toStrRound(r):
    return '\n'.join([toStrResult(g) for g in r]) + toStrBye(r)

def toStrStandings():
    points = {player: 0 for player in names.keys()}
    games = {player: 0 for player in names.keys()}
    gamesAsBlack = {player: 0 for player in names.keys()}
    wins = {player: 0 for player in names.keys()}

    for r in rounds:
        for g in r:
            if g[1] == 'w':
                points[g[0][0]] += 1
                wins[g[0][0]] += 1
            elif g[1] == 'd':
                points[g[0][0]] += 0.5
                points[g[0][1]] += 0.5
            elif g[1] == 'b':
                points[g[0][1]] += 1
                wins[g[0][1]] += 1
            else:
                continue
            games[g[0][0]] += 1
            games[g[0][1]] += 1
            gamesAsBlack[g[0][1]] += 1

    table = list(map(lambda player: (player, getName(player), points[player], games[player], gamesAsBlack[player], wins[player]), sorted(names.keys(), key = lambda player: (points[player], -games[player], gamesAsBlack[player], wins[player]), reverse=True)))

    tableStr = ''

    tableStr += '| Pos | Nome | Pts | J | J P | V |'
    tableStr += '\n'
    tableStr += '| :---: | :--- | :---: | :---: | :---: | :---: |'

    lastI = None
    for i, entry in enumerate(table):
        playersSorted.append(entry[0])
        tableStr += '\n'
        if i == 0 or entry[2:] != table[i - 1][1:]:
            tableStr += f'| {i + 1} | {" | ".join(map(str, entry[1:]))} |'
            lastI = i
        else:
            tableStr += f'| {lastI + 1} | {" | ".join(map(str, entry[1:]))} |'

    return tableStr

def toStrCrossLine(cod):
    lineStr = ''

    lineStr += f'| {getName(cod)} '

    points = 0
    for player in playersSorted:
        if player == cod:
            lineStr += f'| :::::::: '
            continue

        for r in rounds:
            for g in r:
                if g[0][1] == cod and g[0][0] == player:
                    if g[1] == 'w':
                        result = '0'
                    elif g[1] == 'd':
                        result = '0.5'
                        points += 0.5
                    elif g[1] == 'b':
                        result = '1'
                        points += 1
                    else:
                        result = ''

        # Feito duas vezes, para caso seja ida-volta, ele coloque na horizontal os resultados de brancas, senão (só ida), qualquer um.
        for r in rounds:
            for g in r:
                if g[0][0] == cod and g[0][1] == player:
                    if g[1] == 'w':
                        result = '1'
                        points += 1
                    elif g[1] == 'd':
                        result = '0.5'
                        points += 0.5
                    elif g[1] == 'b':
                        result = '0'
                    else:
                        result = ''

        lineStr += f'| {result} '

    lineStr += f'| {points} '
    lineStr += '|'

    return lineStr

def toStrCrossTable():
    tableStr = ''

    tableStr += '| | ' + ' | '.join([getAbbreviation(player) for player in playersSorted]) + ' | Pts |'
    tableStr += '\n'
    tableStr += '| :--- | ' + ' | '.join([':---:' for player in playersSorted]) + ' | :---: |'
    tableStr += '\n'
    tableStr += '\n'.join([toStrCrossLine(player) for player in playersSorted])

    return tableStr


page = ''

if currentRound != None:
    page += '### Rodada atual:'
    page += '\n'
    page += toStrRound(rounds[currentRound])
    page += '\n'
    page += '\n'

if lastRound != None:
    page += '### Rodada anterior:'
    page += '\n'
    page += toStrRound(rounds[lastRound])
    page += '\n'
    page += '\n'

if nextRound != None:
    page += '### Rodada seguinte:'
    page += '\n'
    page += toStrRound(rounds[nextRound])
    page += '\n'
    page += '\n'

page += '## Tabela'
page += '\n'
page += '\n'
page += toStrStandings()
page += '\n'
page += '\n'

page += '## Resultados'
page += '\n'
page += '\n'
page += toStrCrossTable()
page += '\n'
page += '\n'

for i, r in enumerate(rounds):
    page += f'### Rodada {i + 1}:'
    page += '\n'
    page += toStrRound(r)
    page += '\n'
    page += '\n'

open('index.md', 'w').write(page)