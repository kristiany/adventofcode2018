import collections

inputs = [
    '418 players; last marble is worth 71339 points',
    '418 players; last marble is worth 7133900 points'
    ]
test_inputs = [
    '9 players; last marble is worth 25 points',
    '10 players; last marble is worth 1618 points',
    '13 players; last marble is worth 7999 points',
    '17 players; last marble is worth 1104 points',
    '21 players; last marble is worth 6111 points',
    '30 players; last marble is worth 5807 points'
    ]


input_nr = 1
for input in inputs:
    words = input.split(' ')
    nr_of_players = int(words[0])
    points = int(words[6])
    marble = 1
    circle = collections.deque()
    circle.append(0)
    scores = [0] * nr_of_players
    current_player = 0
    while marble <= points:
        if marble % 23 == 0:
            scores[current_player] += marble
            circle.rotate(7)
            scores[current_player] += circle.popleft()
        else:
            circle.rotate(-2)
            circle.appendleft(marble)
        marble += 1
        current_player = (current_player + 1) % nr_of_players
    print('Part {}: score {}'.format(input_nr, max(scores)))
    input_nr += 1
