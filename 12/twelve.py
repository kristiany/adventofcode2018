with open('input.txt', 'r') as file:
    data = file.read()

generations = 200


def rules(input):
    lines = input.strip().split('\n')
    init = lines[0].split(':')[1].strip()
    result = {}
    for line in lines[2:]:
        parts = line.split('=>')
        rule = parts[0].strip()
        result[rule] = parts[1].strip()
    return init, result


def evolve(start_index, gen, new_gen, grammar):
    key = ''.join(gen[start_index: start_index + 5])
    result = '.'
    if key in grammar:
        result = grammar[key]
    new_gen[start_index + 2] = result


def generation_sum(zero, gen):
    return sum([i - zero for i, x in enumerate(gen) if x == '#'])


initial, grammar = rules(data)
gen = ['.'] * 3 + list(initial) + ['.'] * 3
print("{}: {}".format('  0', ''.join(gen)))
zero = 3
gen_sum = [generation_sum(zero, gen)]
for g in range(1, generations + 1):
    temp_gen = gen.copy()
    for j in range(len(temp_gen) - 5):
        evolve(j, gen, temp_gen, grammar)
    print("{}: {}".format(('' if g > 99 else ' ' if g > 9 else '  ') + str(g), ''.join(temp_gen)))
    gen = temp_gen + ['.']
    gen_sum.append(generation_sum(zero, gen))
    if g > 10 and len(set([gen_sum[i] - gen_sum[i - 1] for i in range(g - 10, g + 1)])) == 1:
        print("Population growth stabilised for 10 last generations by {}".format(gen_sum[g] - gen_sum[g - 1]))
        break

print("Part 1: plants sum {}".format(gen_sum[20]))

plants = generation_sum(zero, gen)
last_gen = len(gen_sum) - 1
stable_growth = gen_sum[last_gen - 1] - gen_sum[last_gen - 2]
fiftybillion_sum = plants + stable_growth * (50000000000 - last_gen)
print("Part 2: plants sum for generation fifty billion is {}".format(fiftybillion_sum))
