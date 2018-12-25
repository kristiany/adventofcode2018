with open('input.txt', 'r') as file:
    data = file.read()


def to_numbers(input):
    result = []
    for nr in input.strip().split(' '):
        result.append(int(nr))
    return result


def sum_metadata(nrs, node_start):
    nr_of_children = nrs[node_start]
    nr_of_meta = nrs[node_start + 1]
    result = 0
    next_pos = node_start + 2
    for i in range(nr_of_children):
        sub_sum, next_pos = sum_metadata(nrs, next_pos)
        result += sub_sum
    last_pos = next_pos + nr_of_meta
    for i in range(next_pos, last_pos):
        result += nrs[i]
    return result, last_pos


def value(nrs, node_start):
    nr_of_children = nrs[node_start]
    nr_of_meta = nrs[node_start + 1]
    next_pos = node_start + 2
    children_values = []
    for i in range(nr_of_children):
        sub_value, next_pos = value(nrs, next_pos)
        children_values.append(sub_value)
    last_pos = next_pos + nr_of_meta

    result = 0
    if nr_of_children == 0:
        for i in range(next_pos, last_pos):
            result += nrs[i]
    else:
        for i in range(next_pos, last_pos):
            if 0 < nrs[i] <= len(children_values):
                result += children_values[nrs[i] - 1]
    return result, last_pos


nrs = to_numbers(data)

print("Part 1: {}".format(str(sum_metadata(nrs, 0)[0])))
print("Part 2: {}".format(str(value(nrs, 0)[0])))