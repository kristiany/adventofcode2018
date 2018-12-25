import re
import collections

with open('input.txt', 'r') as file:
    data = file.read()

cart_pattern = re.compile(r'[><v^]')
dirs = ['^', '>', 'v', '<']
dup = (0, -1)
ddown = (0, 1)
dleft = (-1, 0)
dright = (1, 0)


def tracks_n_carts(input):
    lines = input.split('\n')
    map = []
    carts = []
    y = 0
    for line in lines:
        row = list(line)
        for m in cart_pattern.finditer(line):
            index = m.start()
            c = row[index]
            if c == '<' or c == '>':
                row[index] = '-'
            else:
                row[index] = '|'
            carts.append({
                'dir': dirs.index(c),
                'pos': (index, y),
                'turn': 0,
                'crashed': False
            })
        map.append(row)
        y += 1
    return map, carts


def turn_left(cart):
    cart['dir'] = 3
    return dleft


def turn_right(cart):
    cart['dir'] = 1
    return dright


def turn_up(cart):
    cart['dir'] = 0
    return dup


def turn_down(cart):
    cart['dir'] = 2
    return ddown


def move(cart, map):
    pos = cart['pos']
    current_track = map[pos[1]][pos[0]]
    update = (0, 0)
    if cart['dir'] == 0:  # up
        if current_track == '|':
            update = dup
        elif current_track == '/':
            update = turn_right(cart)
        elif current_track == '\\':
            update = turn_left(cart)
        elif current_track == '+':
            turn = cart['turn']
            cart['turn'] = (cart['turn'] + 1) % 3
            if turn == 0:
                update = turn_left(cart)
            elif turn == 2:
                update = turn_right(cart)
            else:
                update = dup
        else:
            raise Exception("Illegal state {} on track {}".format(cart, current_track))
    elif cart['dir'] == 2:  # down
        if current_track == '|':
            update = ddown
        elif current_track == '/':
            update = turn_left(cart)
        elif current_track == '\\':
            update = turn_right(cart)
        elif current_track == '+':
            turn = cart['turn']
            cart['turn'] = (cart['turn'] + 1) % 3
            if turn == 0:
                update = turn_right(cart)
            elif turn == 2:
                update = turn_left(cart)
            else:
                update = ddown
        else:
            raise Exception("Illegal state {} on track {}".format(cart, current_track))
    elif cart['dir'] == 1:  # right
        if current_track == '-':
            update = dright
        elif current_track == '/':
            update = turn_up(cart)
        elif current_track == '\\':
            update = turn_down(cart)
        elif current_track == '+':
            turn = cart['turn']
            cart['turn'] = (cart['turn'] + 1) % 3
            if turn == 0:
                update = turn_up(cart)
            elif turn == 2:
                update = turn_down(cart)
            else:
                update = dright
        else:
            raise Exception("Illegal state {} on track {}".format(cart, current_track))
    elif cart['dir'] == 3:  # left
        if current_track == '-':
            update = dleft
        elif current_track == '/':
            update = turn_down(cart)
        elif current_track == '\\':
            update = turn_up(cart)
        elif current_track == '+':
            turn = cart['turn']
            cart['turn'] = (cart['turn'] + 1) % 3
            if turn == 0:
                update = turn_down(cart)
            elif turn == 2:
                update = turn_up(cart)
            else:
                update = dleft
        else:
            raise Exception("Illegal state {} on track {}".format(cart, current_track))
    cart['pos'] = (cart['pos'][0] + update[0], cart['pos'][1] + update[1])


def detect_collisions(carts):
    positions = [c['pos'] for c in carts]
    unique_positions = set(positions)
    result = []
    if len(unique_positions) != len(positions):
        for p in [p for p, count in collections.Counter(positions).items() if count > 1]:
            for c in carts:
                if c['pos'] == p:
                    c['crashed'] = True
                    result.append(c)
    return result


map, carts = tracks_n_carts(data)
for line in map:
    print(''.join(line))
print(carts)
collisions = []
active_carts = carts.copy()
tick = 1
while len(active_carts) > 1:
    active_carts.sort(key=lambda c: c['pos'][1])
    for cart in active_carts:
        if not cart['crashed']:
            move(cart, map)
            collisions += detect_collisions(active_carts)
    active_carts = [c for c in active_carts if not c['crashed']]
    tick += 1

print("Part 1: first crash at {}".format(collisions[0]['pos']))

if len(active_carts) > 0:
    print("Part 2: last cart left at {}".format(active_carts[0]['pos']))
else:
    print("Part 2: no cart left")
