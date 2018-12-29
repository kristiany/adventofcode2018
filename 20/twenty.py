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
        return furthest_path(path[0: start_group] + \
                             furthest_path(path[start_group + 1: end_group]) + \
                             path[end_group + 1:])
    options = path.find('|')
    if options >= 0:
        choices = set(path.split('|'))
        #print(choices)
        if '' in choices:
            return ''
        return max([furthest_path(c) for c in choices], key=len)
    return path


path = furthest_path(data[1: len(data) - 1])
print(path)
print("Part 1: path to the furthest room is {} doors away".format(len(path)))


