with open('input.txt', 'r') as file:
    data = file.read()


def read(input):
    lines = input.strip().split('\n')
    samples = []
    sample = None
    program = []
    for line in lines:
        clean = line.strip()
        if len(clean) > 0:
            if clean.startswith('Before'):
                sample = {'before': parse_nrs(clean)}
            elif clean.startswith('After'):
                sample['after'] = parse_nrs(clean)
                samples.append(sample)
                sample = None
            elif sample is not None:
                sample['ins'] = [int(c.strip()) for c in clean.split(' ')]
            else:
                program.append([int(c.strip()) for c in clean.split(' ')])
    return samples, program


def parse_nrs(clean):
    return [int(c.strip()) for c in clean.split('[')[1].replace(']', '').split(',')]


def test_addr(ra, rb, c, regs):
    return regs[ra] + regs[rb] == c


def test_addi(ra, b, c, regs):
    return regs[ra] + b == c


def test_mulr(ra, rb, c, regs):
    return regs[ra] * regs[rb] == c


def test_muli(ra, b, c, regs):
    return regs[ra] * b == c


def test_banr(ra, rb, c, regs):
    return regs[ra] & regs[rb] == c


def test_bani(ra, b, c, regs):
    return regs[ra] & b == c


def test_borr(ra, rb, c, regs):
    return regs[ra] | regs[rb] == c


def test_bori(ra, b, c, regs):
    return regs[ra] | b == c


def test_setr(ra, rb, c, regs):
    return regs[ra] == c


def test_seti(a, b, c, regs):
    return a == c


def test_gtir(a, rb, c, regs):
    return (1 if a > regs[rb] else 0) == c


def test_gtri(ra, b, c, regs):
    return (1 if regs[ra] > b else 0) == c


def test_gtrr(ra, rb, c, regs):
    return (1 if regs[ra] > regs[rb] else 0) == c


def test_eqir(a, rb, c, regs):
    return (1 if a == regs[rb] else 0) == c


def test_eqri(ra, b, c, regs):
    return (1 if regs[ra] == b else 0) == c


def test_eqrr(ra, rb, c, regs):
    return (1 if regs[ra] == regs[rb] else 0) == c


def run_addr(ra, rb, c, regs):
    regs[c] = regs[ra] + regs[rb]
    return regs


def run_addi(ra, b, c, regs):
    regs[c] = regs[ra] + b
    return regs


def run_mulr(ra, rb, c, regs):
    regs[c] = regs[ra] * regs[rb]
    return regs


def run_muli(ra, b, c, regs):
    regs[c] = regs[ra] * b
    return regs


def run_banr(ra, rb, c, regs):
    regs[c] = regs[ra] & regs[rb]
    return regs


def run_bani(ra, b, c, regs):
    regs[c] = regs[ra] & b
    return regs


def run_borr(ra, rb, c, regs):
    regs[c] = regs[ra] | regs[rb]
    return regs


def run_bori(ra, b, c, regs):
    regs[c] = regs[ra] | b
    return regs


def run_setr(ra, rb, c, regs):
    regs[c] = regs[ra]
    return regs


def run_seti(a, b, c, regs):
    regs[c] = a
    return regs


def run_gtir(a, rb, c, regs):
    regs[c] = 1 if a > regs[rb] else 0
    return regs


def run_gtri(ra, b, c, regs):
    regs[c] = 1 if regs[ra] > b else 0
    return regs


def run_gtrr(ra, rb, c, regs):
    regs[c] = 1 if regs[ra] > regs[rb] else 0
    return regs


def run_eqir(a, rb, c, regs):
    regs[c] = 1 if a == regs[rb] else 0
    return regs


def run_eqri(ra, b, c, regs):
    regs[c] = 1 if regs[ra] == b else 0
    return regs


def run_eqrr(ra, rb, c, regs):
    regs[c] = 1 if regs[ra] == regs[rb] else 0
    return regs


test_functions = [test_addr, test_addi, test_mulr, test_muli, test_banr, test_bani, test_borr, test_bori,
                  test_setr, test_seti, test_gtir, test_gtri, test_gtrr, test_eqir, test_eqri, test_eqrr]
run_functions = [run_addr, run_addi, run_mulr, run_muli, run_banr, run_bani, run_borr, run_bori,
                 run_setr, run_seti, run_gtir, run_gtri, run_gtrr, run_eqir, run_eqri, run_eqrr]


def test(sample):
    result = []
    for f in test_functions:
        result.append(f(sample['ins'][1], sample['ins'][2], sample['after'][sample['ins'][3]], sample['before']))
    print("Sample {} matches {}".format(sample,
                                        ', '.join([test_functions[i].__name__ for i, v in enumerate(result) if v])))
    return result


def f_names(op, matches):
    return [run_functions[i].__name__ for i in matches[op]]


def print_matches(matches):
    for op in sorted(matches.keys()):
        print("{}: {}".format(str(op), ', '.join(f_names(op, matches))))


more_than_three = 0
samples, program = read(data)
operations = {}
for sample in samples:
    result = test(sample)
    if len([r for r in result if r]) >= 3:
        more_than_three += 1
    op = sample['ins'][0]
    matching_ops = set([i for i, v in enumerate(result) if v])
    if op not in operations:
        operations[op] = matching_ops
    else:
        operations[op] = operations[op].intersection(matching_ops)

print("Part 1: {} / {} samples match more than three ops".format(more_than_three, len(samples)))

done = set()
iteration = 1
#print_matches(operations)
while len(done) < 16:
    #print("Iteration {}".format(iteration))
    for op in operations.keys() - done:
        if len(operations[op]) == 1:
            for m in operations.keys() - [op]:
                operations[m] = operations[m] - operations[op]
            done.add(op)
    #print_matches(operations)
    iteration += 1

print_matches(operations)
for op in operations:
    operations[op] = operations[op].pop()

registers = [0, 0, 0, 0]
for line in program:
    op = operations[line[0]]
    registers = run_functions[op](line[1], line[2], line[3], registers)

print("Part 2: final registers {}".format(' '.join([str(r) for r in registers])))
