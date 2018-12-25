import os


GOBLIN_POWER = 3

with open('input.txt', 'r') as file:
    data = file.read()


def world(input):
    lines = input.strip().split('\n')
    map = []
    goblins = []
    elves = []
    for y, line in enumerate(lines):
        map.append(list(line))
        for x, c in enumerate(line):
            if c == 'E':
                elves.append({
                    'pos': (x, y),
                    'dead': False,
                    'hp': 200
                })
            if c == 'G':
                goblins.append({
                    'pos': (x, y),
                    'dead': False,
                    'hp': 200
                })
    return map, goblins, elves


def printm(map, living):
    for i, row in enumerate(map):
        cs_on_row = sorted([c for c in living if i == c['pos'][1]], key=lambda k: k['pos'][0])
        print("{} {}".format(''.join(row), ' '.join(['('+str(c['hp'])+')' for c in cs_on_row])))



def adjacent_to(pos, e):
    ex = e['pos'][0]
    ey = e['pos'][1]
    return pos[0] == ex and (ey - 1 == pos[1] or ey + 1 == pos[1]) \
           or pos[1] == ey and (ex - 1 == pos[0] or ex + 1 == pos[0])


def unit_type(u, map):
    return map[u['pos'][1]][u['pos'][0]]


def enemies_in_range(c, order, map):
    current_unit = unit_type(c, map)
    enemy = 'G' if current_unit == 'E' else 'E'
    return [e for e in order if
            not e['dead'] and unit_type(e, map) == enemy and adjacent_to((c['pos'][0], c['pos'][1]), e)]


def attack(adjacents, map, attack_power):
    order = sorted(adjacents, key=lambda k: (k['hp'], k['pos'][1], k['pos'][0]))
    weakest = order[0]
    weakest['hp'] -= attack_power
    if weakest['hp'] <= 0:
        weakest['dead'] = True
        map[weakest['pos'][1]][weakest['pos'][0]] = '.'


def attack_if_possible(c, order, map, elf_power):
    current_unit = unit_type(c, map)
    adjacents = enemies_in_range(c, order, map)
    if len(adjacents) > 0:
        attack(adjacents, map, elf_power if current_unit == 'E' else GOBLIN_POWER)
        return True
    return False


def closest_available_to(x, y, map):
    result = []
    if y > 1 and map[y - 1][x] == '.':
        result.append((x, y - 1))
    if y < len(map) - 1 and map[y + 1][x] == '.':
        result.append((x, y + 1))
    if x > 1 and map[y][x - 1] == '.':
        result.append((x - 1, y))
    if x < len(map[0]) - 1 and map[y][x + 1] == '.':
        result.append((x + 1, y))
    return result


def find_closest_path(from_pos, current_unit, order, map):
    enemies = [c for c in order if not c['dead'] and unit_type(c, map) != current_unit]
    available_target_positions = []
    for e in enemies:
        x = e['pos'][0]
        y = e['pos'][1]
        available_target_positions += closest_available_to(x, y, map)
    targets = sorted(available_target_positions, key=lambda k: (k[1], k[0]))
    target_shortest = []
    target_dists = []
    for i, target in enumerate(targets):
        shortest_paths = []
        shortest_dist = 9999999
        for start in closest_available_to(from_pos[0], from_pos[1], map):
            path = closest_path(start, target, map)
            if 0 < len(path) < shortest_dist:
                shortest_dist = len(path)
                shortest_paths = [path]
            elif len(path) == shortest_dist:
                shortest_paths.append(path)
        target_shortest.append(shortest_paths)
        target_dists.append(shortest_dist)
    dist = 9999999
    best_target = -1
    for i, target in enumerate(targets):
        if 0 < target_dists[i] < dist:
            dist = target_dists[i]
            best_target = i
    if best_target < 0:
        return None
    paths = target_shortest[best_target]
    if len(paths) == 0:
        return None
    possible_steps = sorted([x[0] for x in paths], key=lambda k: (k[1], k[0]))
    return possible_steps[0]


def taxi_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# https://en.wikipedia.org/wiki/A*_search_algorithm
def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


def closest_path(start, goal, map):
    closed = set()
    open = set()
    open.add(start)
    came_from = {}
    gscore = {start: 0}
    fscore = {start: taxi_distance(start, goal)}
    while len(open) > 0:
        current = sorted(list(open), key=lambda k: (fscore[k]))[0]
        if current == goal:
            return reconstruct_path(came_from, current)
        open.remove(current)
        closed.add(current)
        for neighbor in closest_available_to(current[0], current[1], map):
            if neighbor in closed:
                continue
            tentative_gscore = gscore[current] + 1
            if neighbor not in open:
                open.add(neighbor)
            elif tentative_gscore >= gscore[neighbor]:
                continue
            came_from[neighbor] = current
            gscore[neighbor] = tentative_gscore
            fscore[neighbor] = gscore[neighbor] + taxi_distance(neighbor, goal)
    return []


def move(c, to, map):
    map[to[1]][to[0]] = unit_type(c, map)
    map[c['pos'][1]][c['pos'][0]] = '.'
    c['pos'] = to


def fight_over(elves, goblins, full_rounds):
    if len([x for x in elves if not x['dead']]) == 0:
        print("All elves died, at {} full rounds".format(full_rounds))
        hps = sum([g['hp'] for g in goblins if not g['dead']])
        print("Sum of goblin hps {} and battle outcome {}".format(hps, full_rounds * hps))
        print(sorted(goblins, key=lambda k: (k['pos'][1], k['pos'][0])))
        printm(map, [c for c in elves + goblins if not c['dead']])
        return True
    if len([x for x in goblins if not x['dead']]) == 0:
        print("All goblins died, at {} full rounds".format(full_rounds))
        hps = sum([e['hp'] for e in elves if not e['dead']])
        print("Sum of elves hps {} and battle outcome {}".format(hps, (full_rounds) * hps))
        print(sorted(elves, key=lambda k: (k['pos'][1], k['pos'][0])))
        printm(map, [c for c in elves + goblins if not c['dead']])
        return True
    return False


def battle(elf_power, map, goblins, elves):
    full_round = 0
    while 1:
        print("Starting round {}".format(full_round + 1))
        living = [c for c in elves + goblins if not c['dead']]
        order = sorted(living, key=lambda k: (k['pos'][1], k['pos'][0]))
        for c in order:
            if not c['dead']:
                if fight_over(elves, goblins, full_round):
                    break
                if not attack_if_possible(c, order, map, elf_power):
                    next_step = find_closest_path(c['pos'], unit_type(c, map), order, map)
                    if next_step is not None:
                        move(c, next_step, map)
                        attack_if_possible(c, order, map, elf_power)
        else:
            full_round += 1
            #os.system('clear')
            #printm(map, [c for c in elves + goblins if not c['dead']])

            continue
        break
    return [c for c in elves if not c['dead']]


map, goblins, elves = world(data)
printm(map, elves + goblins)
number_of_elves = len(elves)
elf_power = 3
living_elves = battle(elf_power, map, goblins, elves)
while number_of_elves != len(living_elves):
    elf_power += 1
    print("Elf attack power = {}".format(elf_power))
    map, goblins, elves = world(data)
    living_elves = battle(elf_power, map, goblins, elves)
print("Part 2: attack power {} keeps all elves alive".format(elf_power))