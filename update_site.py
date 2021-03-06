import sys
import pathlib
projectFolder = pathlib.Path(__file__).parent.absolute()
sys.path.insert(0, 'E:/Programas/Programas em Python')
sys.path.insert(0, f'{projectFolder}/source')

import os
from tournament import Tournament
from player import Player
from mylib import save, load

def main():
    data = open(f'{projectFolder}/data.txt', encoding='utf-8').read().split('\n')

    players = []

    analysing = None
    for line in data:
        if line.startswith('\t'):
            pass
        elif line.endswith(':'):
            analysing = line[:-1]
        elif analysing == 'c' and '=' in line:
            for code in line[1:].split(','):
                players.append(Player(code, data))

    cache = load(f'{projectFolder}/cache') or {}

    tournaments = [Tournament('rapid', data, 0, players, cache), Tournament('blitz', data, 1, players, cache)]

    save(f'{projectFolder}/cache', cache)

    for tournament in tournaments:
        tournament.compute_stats()

    number_of_rounds = data.count('r:')

    last_round = None
    current_round = None
    next_round = None

    for i in range(number_of_rounds):
        if not tournaments[0].rounds[i].closed or not tournaments[1].rounds[i].closed:
            current_round = i
            if i > 0:
                last_round = i - 1
            if i < number_of_rounds - 1:
                next_round = i + 1
            break
    else:
        last_round = number_of_rounds - 1

    page = ''

    page += '***`Torneio todos-contra-todos, entre 13 participantes, com partidas 15+5 e 5+4.`***'
    page += '\n'
    page += '\n'
    page += '## Participantes:'
    page += '\n'
    page += '\n'
    page += '\n'.join(map(lambda player: '* ' + player.resume(['rapid', 'blitz']), sorted(players, key=lambda player: player.name)))
    page += '\n'
    page += '\n'

    page += '## Rodadas:'
    page += '\n'
    page += '\n'

    if current_round != None:
        page += f'* [Rodada atual](https://grupo-de-xadrez.github.io/rodadas/{current_round+1})'
        page += '\n'
        page += '\n'

    if last_round != None:
        page += f'* [Rodada anterior](https://grupo-de-xadrez.github.io/rodadas/{last_round+1})'
        page += '\n'
        page += '\n'

    if next_round != None:
        page += f'* [Rodada seguinte](https://grupo-de-xadrez.github.io/rodadas/{next_round+1})'
        page += '\n'
        page += '\n'

    page += f'* [Lista completa](https://grupo-de-xadrez.github.io/rodadas)'
    page += '\n'
    page += '\n'

    page += '## Tabelas'
    page += '\n'
    page += '\n'

    page += '#### Rapid'
    page += '\n'
    page += '\n'
    page += tournaments[0].table()
    page += '\n'
    page += '\n'

    page += '#### Blitz'
    page += '\n'
    page += '\n'
    page += tournaments[1].table()
    page += '\n'
    page += '\n'

    open(f'{projectFolder}/index.md', 'w', encoding='utf-8').write(page)

    if not os.path.exists(f'{projectFolder}/rodadas/'):
        os.mkdir(f'{projectFolder}/rodadas/')

    subpage = '### [\u2302 Página Principal](https://grupo-de-xadrez.github.io/)'
    subpage += '\n'
    subpage += '\n'
    subpage += '## Rodadas:'
    subpage += '\n'
    subpage += '\n'

    for i in range(number_of_rounds):
        subsubpage = '### [\u2302 Página Principal](https://grupo-de-xadrez.github.io/)'
        subsubpage += '\n'
        subsubpage += '\n'
        subsubpage += f'### Rodada {i + 1}:'
        subsubpage += '\n'
        subsubpage += '\n'
        subsubpage += '#### Rapid:'
        subsubpage += '\n'
        subsubpage += '\n'
        subsubpage += str(tournaments[0].rounds[i])
        subsubpage += '\n'
        subsubpage += '\n'
        subsubpage += '#### Blitz:'
        subsubpage += '\n'
        subsubpage += '\n'
        subsubpage += str(tournaments[1].rounds[i])
        subsubpage += '\n'
        subsubpage += '\n'

        if not os.path.exists(f'{projectFolder}/rodadas/{i+1}/'):
            os.mkdir(f'{projectFolder}/rodadas/{i+1}/')

        open(f'{projectFolder}/rodadas/{i+1}/index.md', 'w', encoding='utf-8').write(subsubpage)

        subpage += f'* [Rodada {i + 1}](https://grupo-de-xadrez.github.io/rodadas/{i+1})'
        subpage += '\n'
        subpage += '\n'

    open(f'{projectFolder}/rodadas/index.md', 'w', encoding='utf-8').write(subpage)

if __name__ == '__main__':
    main()
