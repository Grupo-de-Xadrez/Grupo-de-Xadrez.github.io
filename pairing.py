x = ''

players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', ' ']

count = {player: 0 for player in players}

from random import randint

for j in range(1, 26+1):
    for i in range(7):
        if f'{players[i]} x {players[i + 7]}\n' in x:
            x += f'{players[i + 7]} x {players[i]}\n'
            count[players[i + 7]] += 1
            continue

        if f'{players[i + 7]} x {players[i]}\n' in x:
            x += f'{players[i]} x {players[i + 7]}\n'
            count[players[i]] += 1
            continue

        if count[players[i]] + randint(0, 1) > count[players[i + 7]]:
        # if count[players[i]] > count[players[i + 7]]:
            x += f'{players[i + 7]} x {players[i]}\n'
            count[players[i + 7]] += 1
            continue
        else:
            x += f'{players[i]} x {players[i + 7]}\n'
            count[players[i]] += 1
            continue

    x += '\n'
    players = players[0:1] + players[7:8] + players[1:6] + players[8:14] + players[6:7]
    if j == 13:
        print(sorted(count.values()))

open('pairing.txt', 'w').write(x)

x = open('pairing.txt', 'r').read().split('\n')[:-2]

y = 'r:'

for l in x:
    if l == '':
        y += '\n\nr:'
    elif l[0] == ' ' or l[-1] == ' ':
        pass
    else:
        y += f'\n{l[0]},{l[-1]}=,'

open('ndata.txt', 'w').write(y)
