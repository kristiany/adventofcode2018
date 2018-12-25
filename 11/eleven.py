input = 7689
test_input = 42
serial_nr = input


def rack_id(x):
    return x + 10


def power_level(rid, y):
    return rid * y


def hundreds(nr):
    string = str(nr)
    if len(string) < 3:
        return 0
    return int(string[::-1][2])


def total(grid, x, y, size):
    result = 0
    for s in range(size):
        result += sum(grid[y + s][x: x + size])
    return result


def total_extended(grid, x, y, power_size):
    result = 0
    for s in range(power_size):
        result += grid[y + s][x + power_size - 1]
    return result + sum(grid[y + power_size - 1][x: x + power_size - 1])


size = 300
grid = [[] for _ in range(size)]
for y in range(size):
    for x in range(size):
        rid = rack_id(x + 1)
        power = hundreds((power_level(rid, y + 1) + serial_nr) * rid) - 5
        grid[y].append(power)


maxp = -100000
maxcoord = 0, 0
for y in range(size - 2):
    for x in range(size - 2):
        t = total(grid, x, y, 3)
        if maxp < t:
            maxp = t
            maxcoord = x + 1, y + 1

print("Part 1: max power {} at {}".format(maxp, maxcoord))


maxp = -100000
maxcoord = 0, 0, 0
for y in range(size):
    for x in range(size):
        last_total = total(grid, x, y, 1)
        for power_size in range(2, 301):
            if x + power_size > size or y + power_size > size:
                break
            t = last_total + total_extended(grid, x, y, power_size)
            last_total = t
            if maxp < t:
                maxp = t
                maxcoord = x + 1, y + 1, power_size
print("Part 2: max power {} at {}".format(maxp, maxcoord))