with open('input.txt', 'r') as file:
    data = file.read()


def read(input):
    lines = input.strip().split('\n')
    ip = int(lines[0].split(' ')[1])
    program = []
    for line in lines[1:]:
        parts = line.split(' ')
        f = parts[0]
        a = int(parts[1])
        b = int(parts[2])
        c = int(parts[3])
        program.append((f, a, b, c))
    return ip, program


def addr(ra, rb, c, regs):
    regs[c] = regs[ra] + regs[rb]
    return regs


def addi(ra, b, c, regs):
    regs[c] = regs[ra] + b
    return regs


def mulr(ra, rb, c, regs):
    regs[c] = regs[ra] * regs[rb]
    return regs


def muli(ra, b, c, regs):
    regs[c] = regs[ra] * b
    return regs


def banr(ra, rb, c, regs):
    regs[c] = regs[ra] & regs[rb]
    return regs


def bani(ra, b, c, regs):
    regs[c] = regs[ra] & b
    return regs


def borr(ra, rb, c, regs):
    regs[c] = regs[ra] | regs[rb]
    return regs


def bori(ra, b, c, regs):
    regs[c] = regs[ra] | b
    return regs


def setr(ra, rb, c, regs):
    regs[c] = regs[ra]
    return regs


def seti(a, b, c, regs):
    regs[c] = a
    return regs


def gtir(a, rb, c, regs):
    regs[c] = 1 if a > regs[rb] else 0
    return regs


def gtri(ra, b, c, regs):
    regs[c] = 1 if regs[ra] > b else 0
    return regs


def gtrr(ra, rb, c, regs):
    regs[c] = 1 if regs[ra] > regs[rb] else 0
    return regs


def eqir(a, rb, c, regs):
    regs[c] = 1 if a == regs[rb] else 0
    return regs


def eqri(ra, b, c, regs):
    regs[c] = 1 if regs[ra] == b else 0
    return regs


def eqrr(ra, rb, c, regs):
    regs[c] = 1 if regs[ra] == regs[rb] else 0
    return regs


def execute(program, registers, ip_bound, halt_on_search_start):
    ip = 0
    while 1:
        #print(ip)
        op = program[ip]
        #print(op)
        f = globals()[op[0]]
        registers[ip_bound] = ip
        registers = f(op[1], op[2], op[3], registers)
        ip = registers[ip_bound]
        ip += 1
        #print(registers)
        if ip >= len(program):
            print("Terminated")
            break
        if halt_on_search_start and registers[2:5] == [1, 1, 1]:
            print("Reached running state {}".format(registers))
            break
    return registers


ip_bound, program = read(data)
registers = execute(program, [0] * 6, ip_bound, False)
print("Part 1: value of register 0: {}".format(registers[0]))


registers = execute(program, [1] + [0] * 5, ip_bound, True)
target = registers[5]
evenly_divides = []
for i in range(1, target + 1):
    if target % i == 0:
        evenly_divides.append(i)
print("Part 2: value of register 0: {}".format(sum(evenly_divides)))

