with open('input.txt', 'r') as file:
    data = file.read()


def read(input):
    lines = input.strip().split('\n')
    coords = []
    for line in lines:
        split = line.split(',')
        first = split[0]
        second = split[1]
        c1 = first.split('=')[0]
        v1 = int(first.split('=')[1])
        c2 = second.split('=')[0].strip()
        range = [int(r) for r in second.split('=')[1].split('..')]
        coords.append({
            c1: v1,
            c2: range,
            'range': c2
        })
    return coords


def print_map(map, min_x, size_x):
    first_row = ['.' for _ in range(size_x)]
    first_row[500 - min_x] = '+'
    print("   + {}".format(''.join(first_row)))
    for y, row in enumerate(map):
        print("{:04} {}".format(y, ''.join(row)))


def find_left(x, y):
    for j in range(x - 1, -1, -1):
        if map[y][j] == '#':
            return j, True
        if map[y + 1][j] != '#' and map[y + 1][j] != '~':
            return j, False
    return 0, False


def find_right(x, y):
    for j in range(x + 1, size_x):
        if map[y][j] == '#':
            return j, True
        if map[y + 1][j] != '#' and map[y + 1][j] != '~':
            return j, False
    return size_x - 1, False


def fill(current_y, x_from, x_to, map, c):
    for j in range(x_from, x_to):
        map[current_y][j] = c



scan = read(data)
min_y = min([v['y'][0] if v['range'] == 'y' else v['y'] for v in scan])
max_y = max([v['y'][1] if isinstance(v['y'], list) else v['y'] for v in scan])
print("Min y: {}, max y: {}".format(min_y, max_y))
min_x = min([v['x'][0] if v['range'] == 'x' else v['x'] for v in scan]) - 1
max_x = max([v['x'][1] if v['range'] == 'x' else v['x'] for v in scan]) + 1
print("Min x: {}, max x: {}".format(min_x, max_x))
size_y = max_y - min_y + 1
size_x = max_x - min_x + 1
map = [['.' for _ in range(size_x)] for _ in range(size_y)]

for s in scan:
    if s['range'] == 'x':
        y = s['y'] - min_y
        x_start = s['x'][0] - min_x
        x_end = s['x'][1] + 1 - min_x
        #print("y: {}->{}, range x: ({}: {})->({}: {})".format(s['y'], y, s['x'][0], s['x'][1], x_start, x_end))
        for x in range(x_start, x_end):
            map[y][x] = '#'
    else:
        x = s['x'] - min_x
        y_start = s['y'][0] - min_y
        y_end = s['y'][1] + 1 - min_y
        #print("x: {}->{}, range y: ({}: {})->({}: {})".format(s['x'], x, s['y'][0], s['y'][1], y_start, y_end))
        for y in range(y_start, y_end):
            map[y][x] = '#'

#print_map(map, min_x, size_x)
y = 0
flows = {500 - min_x: (0, None)}
while y < size_y:
    valid_flows = [x for x in flows if flows[x][0] <= y and (flows[x][1] is None or y <= flows[x][1])]
    for x in sorted(valid_flows):
        if map[y][x] == '|':
            continue
        if map[y][x] == '.':
            map[y][x] = '|'
        elif map[y][x] == '#':
            flows[x] = (flows[x][0], y - 1)
            y_offset = -1
            while 1:
                current_y = y + y_offset
                leftmost, left_is_wall = find_left(x, current_y)
                rightmost, right_is_wall = find_right(x, current_y)
                if left_is_wall:
                    if right_is_wall:
                        fill(current_y, leftmost + 1, rightmost, map, '~')
                    else:
                        fill(current_y, leftmost + 1, rightmost + 1, map, '|')
                        flows[rightmost] = (current_y + 1, None)
                        if current_y < y:
                            y = current_y
                        break
                elif right_is_wall:
                    fill(current_y, leftmost, rightmost, map, '|')
                    flows[leftmost] = (current_y + 1, None)
                    if current_y < y:
                        y = current_y
                    break
                else:
                    fill(current_y, leftmost, rightmost + 1, map, '|')
                    flows[rightmost] = (current_y + 1, None)
                    flows[leftmost] = (current_y + 1, None)
                    if current_y < y:
                        y = current_y
                    break
                y_offset -= 1
    y += 1
    #print(flows)


print_map(map, min_x, size_x)
reach = 0
at_rest = 0
for row in map:
    for x in range(size_x):
        if row[x] == '~':
            at_rest += 1
        if row[x] == '~' or row[x] == '|':
            reach += 1

print("Part 1: {} tiles are reached".format(reach))
print("Part 2: {} tiles will be at rest".format(at_rest))
