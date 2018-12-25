with open('input.txt', 'r') as file:
    data = file.read()


def to_coords(input):
    result = []
    for pair in input.strip().split('\n'):
        s = pair.split(',')
        result.append((int(s[0]), int(s[1])))
    return result


def bounding_box(coords):
    return max([c[0] for c in coords]) + 1, max([c[1] for c in coords]) + 1


def taxicab_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def closest(x, y, coords):
    minimum = 100000000
    min_coord = -1
    min_unique = True
    dists = []
    for i, coord in enumerate(coords):
        dist = taxicab_dist((x, y), coord)
        dists.append(dist)
        #print("({}, {}) dist to {} = {}".format(x, y, coord, dist))
        if dist == minimum:
            min_unique = False
        if dist < minimum:
            minimum = dist
            min_coord = i
            min_unique = True
    return (min_coord if min_unique else -1), dists


def debug(dist_map, bb):
    letters = list(map(chr, range(ord('a'), ord('z') + 1)))
    for y in range(bb[1]):
        for x in range(bb[0]):
            c = dist_map[x + y * bb[0]]
            if c > -1:
                print(letters[c], end=" ")
            else:
                print('.', end=" ")
        print('\n')


coords = to_coords(data)

bb = bounding_box(coords)
dist_map = [-1] * bb[0] * bb[1]
areas = [0] * len(coords)
is_infinite = [False] * len(coords)
safe = []
for y in range(bb[1]):
    for x in range(bb[0]):
        c, dists = closest(x, y, coords)
        dist_map[x + y * bb[0]] = c
        if c > -1:
            areas[c] += 1
            if x == 0 or x == bb[0] - 1 or y == 0 or y == bb[1] - 1:
                is_infinite[c] = True
        total_dist = sum(dists)
        if total_dist < 10000:  # Limit for test is 32
            safe.append(total_dist)


#debug(dist_map, bb)

finite_areas = [x for i, x in enumerate(areas) if not is_infinite[i]]
print("Part 1: largest finite area is {}".format(max(finite_areas)))
print("Part 2: size of safe region is {}".format(len(safe)))

