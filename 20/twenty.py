with open('input.txt', 'r') as file:
    data = file.read().strip()


def find_group_end(path):
    paras = []
    for i, c in enumerate(list(path)):
        if c == '(':
            paras.append(c)
        if c == ')':
            if len(paras) == 0:
                return i
            paras.pop(0)
    return -1


def furthest_path(path):
    start_group = path.find('(')
    if start_group >= 0:
        end_group = start_group + 1 + find_group_end(path[start_group + 1:])
        return furthest_path(path[0: start_group] +
                             furthest_path(path[start_group + 1: end_group]) +
                             path[end_group + 1:])
    options = path.find('|')
    if options >= 0:
        choices = set(path.split('|'))
        # print(choices)
        if '' in choices:
            return ''
        return max([furthest_path(c) for c in choices], key=len)
    return path


def walk(current, door):
    if door == 'N':
        return current[0], current[1] - 1
    if door == 'E':
        return current[0] + 1, current[1]
    if door == 'S':
        return current[0], current[1] + 1
    if door == 'W':
        return current[0] - 1, current[1]
    return current


'''
def count(path, distance):
    start_group = path.find('(')
    if start_group >= 0:
        end_group = start_group + 1 + find_group_end(path[start_group + 1:])
        if distance >= 1000:
            return count(path[0: start_group], distance) + count(path[end_group + 1:], distance + end_group + 1) + \
                   count(path[start_group + 1: end_group], distance + start_group + 1)
        else:
            return count(path[0: start_group] +
                         furthest_path(path[start_group + 1: end_group]) +
                         path[end_group + 1:], distance)
    atomic_path = path.replace('|', '')
    if distance >= 1000:
        return len(atomic_path)
    options = path.find('|')
    if options >= 0:
        choices = set(path.split('|'))
        if '' in choices:
            return 0
        return max(0, max([count(c, distance) for c in choices]) - (1000 - distance))
    diff = len(atomic_path) - (1000 - distance)
    return max(0, diff)


def travel(path, distance, current, rooms):
    #rooms = set()
    #current = (0, 0)
    start_group = path.find('(')
    if start_group >= 0:
        end_group = start_group + 1 + find_group_end(path[start_group + 1:])
        rooms = travel(path[start_group + 1: end_group], distance, current, rooms)
        #return travel(path[0: start_group], current, rooms).union(travel(path[end_group + 1:], current, rooms))
        return travel(path[0: start_group] + path[end_group + 1:], current, rooms)
    if path.find('|') >= 0:
        choices = set(path.split('|')) - {''}
        for c in choices:
            rooms = travel(c, current, rooms)
        return rooms
    it = current
    for door in path:
        it = walk(it, door)
        rooms.add(it)
    return rooms'''


def travel(path, distance, current, rooms):
    start_group = path.find('(')
    if start_group >= 0:
        end_group = start_group + 1 + find_group_end(path[start_group + 1:])
        distance, current, rooms = travel(path[0: start_group], distance, current, rooms)
        distance, current, rooms = travel(path[start_group + 1: end_group], distance, current, rooms)
        return travel(path[end_group + 1:], distance, current, rooms)
    options = path.find('|')
    if options >= 0:
        choices = set(path.split('|'))
        for c in choices - {''}:
            _, _, rooms = travel(c, distance, current, rooms)
        if '' in choices:
            return distance, current, rooms
        return travel(max([furthest_path(c) for c in choices], key=len), distance, current, rooms)
    it_c = current
    for door in path:
        it_c = walk(it_c, door)
        distance += 1
        if distance >= 1000:
            rooms.add((it_c[0], it_c[1]))
    return distance, it_c, rooms


regx = data[1: len(data) - 1]
path = furthest_path(regx)

# print(path[0:1000] + '  ' + path[1000:1010])
# print(regx)
print("Part 1: path to the furthest room is {} doors away".format(len(path)))

# last_segment = path[1000 - 20: 1000]
# from_1000 = regx[regx.find(last_segment) + len(last_segment):]
# print(last_segment)
# print(from_1000)
# rooms = travel(from_1000, (0, 0), {(0, 0)})
distance, current, rooms = travel(path, 0, (0, 0, 0), set())
#print(rooms)
print(distance)
print(current)
print("Part 2: rooms with more than 1000 doors away {}".format(len(rooms)))





# 2670 too low
# 2671 too low
# 10066 too high

# not correcto:
# 7788
# 9590
# 9643
# 9699
# 9725
# 10187
# 10205
