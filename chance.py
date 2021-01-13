data = open('data.txt', encoding='utf-8').read().split('\n')

names = dict()
abreviations = dict()
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

    table = list(map(lambda player: (getName(player), points[player], games[player], gamesAsBlack[player], wins[player]), sorted(names.keys(), key = lambda player: (points[player], -games[player], gamesAsBlack[player], wins[player]), reverse=True)))

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

def toStrCrossLine(cod):
    lineStr = ''

    lineStr += f'| {getName(cod)} '

    points = 0
    for player in names.keys():
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

    tableStr += '| | ' + ' | '.join([getAbbreviation(player) for player in names.keys()]) + ' | Pts |'
    tableStr += '\n'
    tableStr += '| :--- | ' + ' | '.join([':---:' for player in names.keys()]) + ' | :---: |'
    tableStr += '\n'
    tableStr += '\n'.join([toStrCrossLine(player) for player in names.keys()])

    return tableStr

from time import time
from random import choices
start = time()

counter = 0
counterList = dict()

while time() - start < 300:
    rounds_ = []

    for r in rounds:
        r_ = []

        for g in r:
            if g[1] == '':
                r_.append((g[0], choices(population = ['w', 'd', 'b'], weights = [0.5, 0.05, 0.45], k = 1)[0]))
            else:
                r_.append(g)

        rounds_.append(r_)

    points = 0
    points = {player: 0 for player in names.keys()}
    games = {player: 0 for player in names.keys()}
    gamesAsBlack = {player: 0 for player in names.keys()}
    wins = {player: 0 for player in names.keys()}

    for r in rounds_:
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


    table = list(map(lambda player: (player, points[player], games[player], gamesAsBlack[player], wins[player]), sorted(names.keys(), key = lambda player: (points[player], -games[player], gamesAsBlack[player], wins[player]), reverse=True)))

    table = [e[0] for e in table if e[1:] == table[0][1:]]

    counter += 1

    for e in table:
        if e in counterList.keys():
            counterList[e] += 1 / len(table)
        else:
            counterList[e] = 1 / len(table)

counterSorted = sorted([(names[player], counterList.get(player, 0) / counter) for player in names.keys()], key = lambda x: x[1], reverse = True)

print('\n'.join([f'{x[0]:<12} {x[1]:>8.3%}' for x in counterSorted]))