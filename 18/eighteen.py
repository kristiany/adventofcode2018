with open('input.txt', 'r') as file:
    data = file.read()


def read(input):
    lines = input.strip().split('\n')
    result = []
    for line in lines:
        result.append(list(line))
    return result


def adjacents(x, y, map):
    coords = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
              (x - 1, y),                 (x + 1, y),
              (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
    valid_coords = [c for c in coords if 0 <= c[0] < len(map[0]) and 0 <= c[1] < len(map)]
    return [map[c[1]][c[0]] for c in valid_coords]


def tree_growth(x, y, map):
    return len([a for a in adjacents(x, y, map) if a == '|']) >= 3


def lumberyard_growth(x, y, map):
    return len([a for a in adjacents(x, y, map) if a == '#']) >= 3


def stay_lumberyard(x, y, map):
    adjs = adjacents(x, y, map)
    return len([a for a in adjs if a == '#']) > 0 and len([a for a in adjs if a == '|']) > 0


def evolve(x, y, map, evolve_to):
    if map[y][x] == '.' and tree_growth(x, y, map):
        evolve_to[y][x] = '|'
    elif map[y][x] == '|' and lumberyard_growth(x, y, map):
        evolve_to[y][x] = '#'
    elif map[y][x] == '#' and not stay_lumberyard(x, y, map):
        evolve_to[y][x] = '.'


def copy(map):
    copy = []
    for y in range(len(map)):
        copy.append(map[y].copy())
    return copy


def print_map(map):
    for y in range(len(map)):
        print(''.join(map[y]))


def resources(map):
    wooded = 0
    lumberyards = 0
    for y in range(len(map)):
        wooded += len([a for a in map[y] if a == '|'])
        lumberyards += len([a for a in map[y] if a == '#'])
    return wooded, lumberyards


def find_pattern(series):
    if len(series) < 20:
        return None
    for size in range(7, int(len(series) / 2)):
        pattern = series[len(series) - size:]
        repeated = pattern + pattern
        # print("Checking if {} is in {}".format(len(repeated), len(last_woods[0: len(pattern) * 2])))
        if series[len(series) - len(pattern) * 2:] == repeated:
            print("Found pattern {}".format(pattern))
            return pattern
    return None


map = read(data)
print_map(map)
for m in range(1, 11):
    snapshot = copy(map)
    for y in range(len(map)):
        for x in range(len(map[0])):
            evolve(x, y, map, snapshot)
    map = snapshot
    print(m)
    print_map(map)


wooded, lumberyards = resources(map)
print("Part 1: {} * {} = {} in resource value".format(wooded, lumberyards, wooded * lumberyards))

m = 1
map = read(data)
progress = True
last_woods = []
last_lumberyards = []
wooded, lumberyards = resources(map)
last_woods.append(wooded)
last_lumberyards.append(lumberyards)
keep = 100
last_wood = wooded
last_lumberyard = lumberyards
woods_pattern = []
lumberyard_pattern = []
stop = False
while not stop:
    snapshot = copy(map)
    for y in range(len(map)):
        for x in range(len(map[0])):
            evolve(x, y, map, snapshot)
    if len(last_woods) >= keep:
        last_woods.pop(0)
    if len(last_lumberyards) >= keep:
        last_lumberyards.pop(0)
    map = snapshot
    wooded, lumberyards = resources(map)
    last_woods.append(wooded - last_wood)
    last_lumberyards.append(lumberyards - last_lumberyard)
    last_wood = wooded
    last_lumberyard = lumberyards
    print(m)
    m += 1
    #print_map(map)
    woods_pattern = find_pattern(last_woods)
    if woods_pattern is not None:
        lumberyard_pattern = find_pattern(last_lumberyards)
        if lumberyard_pattern is not None:
            stop = True


print("For minute {}: woods {}, lumberyards {}".format(m - 1, last_wood, last_lumberyard))
print("Pattern lengths woods: {} and lumberyards: {}".format(len(woods_pattern), len(lumberyard_pattern)))
full_repeats = int((1000000000 - m) / len(woods_pattern))
rest = (1000000000 - m) % len(woods_pattern)
print("Full repeats {}, with rest {}".format(full_repeats, rest))
woods_sum = sum(woods_pattern)
lumberyard_sum = sum(lumberyard_pattern)
final_woods = last_wood + woods_sum * full_repeats + sum(woods_pattern[0: rest + 1])
final_lumberyards = last_lumberyard + lumberyard_sum * full_repeats + sum(lumberyard_pattern[0: rest + 1])
print("Part 2: final resources {} * {} = {}".format(final_woods, final_lumberyards, final_woods * final_lumberyards))
