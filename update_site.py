data = open('data.txt').read().split('\n')

names = dict()
rounds = list()

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

def toStrResult(cod):
    if cod == 'w':
        return 'Brancas venceram.'
    if cod == 'd':
        return 'Empatou.'
    if cod == 'b':
        return 'Pretas venceram.'
    return ''

def toStrRound(r):
    return '\n'.join([f'* {getName(g[0][0])} vs {getName(g[0][1])} = {toStrResult(g[1])}' for g in r])

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
            else:
                continue
            games[g[0][0]] += 1
            games[g[0][1]] += 1
            gamesAsBlack[g[0][1]] += 1

    table = list(map(lambda player: (getName(player), points[player], games[player], gamesAsBlack[player], wins[player]), sorted(names.keys(), key = lambda player: (points[player], -games[player], gamesAsBlack[player], wins[player]), reverse=True)))

    tableStr = ''

    tableStr += '| Pos | Nome | Pts | J | J P | V |'
    tableStr += '\n'
    tableStr += '| --- | --- | --- | --- | --- | --- |'

    lastI = None
    for i, entry in enumerate(table):
        tableStr += '\n'
        if i == 0 or entry[1:] != table[i - 1][1:]:
            tableStr += f'| {i + 1} | {" | ".join(map(str, entry))} |'
            lastI = i
        else:
            tableStr += f'| {lastI + 1} | {" | ".join(map(str, entry))} |'

    return tableStr

page = ''

page += '# Torneio de Xadrez'
page += '\n'

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

for i, r in enumerate(rounds):
    page += f'### Rodada {i + 1}:'
    page += '\n'
    page += toStrRound(r)
    page += '\n'
    page += '\n'

open('index.md', 'w').write(page)