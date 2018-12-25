with open('input.txt', 'r') as file:
    data = file.read()


def to_dependencies(input):
    result = []
    for line in input.strip().split('\n'):
        s = line.split(' ')
        result.append((s[1], s[7]))
    return result


deps = to_dependencies(data)

graph = {}
for a, b in deps:
    if a not in graph:
        graph[a] = []
    graph[a].append(b)

parents = {}
for a, b in deps:
    if b not in parents:
        parents[b] = []
    parents[b].append(a)

roots = set(graph.keys()) - set([v for vs in graph.values() for v in vs])
print("Root {}".format(roots))


def find_valid(propagation, visited, parents):
    for i, c in enumerate(propagation):
        if c not in parents or len(set(parents[c]) - visited) == 0:
            return i
    raise Exception("Oh noes")


def invalid_valid(propagation, visited, parents):
    result = []
    for c in propagation:
        if c not in parents or len(set(parents[c]) - visited) == 0:
            result.append(c)
    return list(set(propagation) - set(result)), result


for key in graph:
    print("{} -> {}".format(key, graph[key]))

order = []
propagation = sorted(list(roots))
visited = set()
while len(propagation) > 0:
    current = propagation.pop(find_valid(propagation, visited, parents))
    order.append(current)
    visited.add(current)
    if current in graph:
        propagation = propagation + graph[current]
    propagation = sorted(list(set(propagation)))

parallelism = 5
base_time = 60
node_duration = {}
for i, key in enumerate(list(map(chr, range(ord('A'), ord('Z') + 1)))):
    node_duration[key] = i + 1 + base_time


propagation = sorted(list(roots))
visited = set()
workers = [[] for _ in range(parallelism)]
worker_current = [('.', 0)] * parallelism
time = 0
order2 = []
while len(propagation) > 0 or any([x[0] != '.' for x in worker_current]):
    propagation, valid = invalid_valid(propagation, visited, parents)
    for v in valid:
        valid_started = False
        for i in range(parallelism):
            if len(workers[i]) <= time:
                workers[i] += v * node_duration[v]
                valid_started = True
                worker_current[i] = (v, time - 1 + node_duration[v])
                break
        if not valid_started:
            propagation.append(v)
    steps = [len(w) - time if len(w) - time > 0 else 1 for w in workers]
    step = min(steps)
    for i in range(parallelism):
        v, ttl = worker_current[i]
        if ttl < time + step:
            if v != '.':
                visited.add(v)
                order2.append(v)  # order will be by current running not proper alfabetical
                if v in graph:
                    propagation = propagation + graph[v]
                worker_current[i] = ('.', time)
    for i in range(parallelism):
        if len(workers[i]) < time + step:
            workers[i] += '.' * ((time + step) - len(workers[i]))

    propagation = sorted(list(set(propagation)))
    time += step


for i, worker in enumerate(workers):
    print("{}: {}".format(i + 1, worker))

print("Part 1: {}".format(''.join(order)))
print("Part 2: order {}".format(''.join(order2)))
print("Part 2: {} sec".format(max(len(w) for w in workers)))
