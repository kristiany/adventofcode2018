
def to_int_array(nr):
    return [int(x) for x in list(str(nr))]


def evolve(elf, scoreboard):
    return (elf + int(scoreboard[elf]) + 1) % len(scoreboard)


def to_total(e1, e2, scoreboard):
    return str(int(scoreboard[e1]) + int(scoreboard[e2]))


input = '430971'
input_nr = int(input)
scoreboard = '37'
elf1 = 0
elf2 = 1
while len(scoreboard) <= input_nr + 10:
    scoreboard += to_total(elf1, elf2, scoreboard)
    elf1 = evolve(elf1, scoreboard)
    elf2 = evolve(elf2, scoreboard)

print("Part 1: ten after {}".format(scoreboard[input_nr: input_nr + 10]))


scoreboard = '37'
elf1 = 0
elf2 = 1
while 1:
    scoreboard += to_total(elf1, elf2, scoreboard)
    found_index = scoreboard.find(input, len(scoreboard) - len(input) - 1)
    if found_index >= 0:
        print("Part 2: {} found after {} recipes".format(input, found_index))
        break
    elf1 = evolve(elf1, scoreboard)
    elf2 = evolve(elf2, scoreboard)
