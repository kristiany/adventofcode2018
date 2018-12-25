import re

#polymer = 'dabAcCaCBAcCcaDA'

with open('input.txt', 'r') as file:
    polymer = file.read()


def reacts(a, b):
    return a.lower() == b.lower() and (a.islower() and b.isupper() or b.islower() and a.isupper())


def react(polymer):
    index = 0
    result = polymer.strip()
    while index < len(result):
        c = result[index]
        if index > 0 and reacts(c, result[index - 1]):
            result = result[0:index - 1] + result[index + 1:]
            index -= 1
            continue
        if index < len(result) - 1 and reacts(c, result[index + 1]):
            result = result[0:index] + result[index + 2:]
            continue
        index += 1
    return result


reduced = react(polymer)
print("Part 1: Resulting polymer is {} units - '{}'".format(len(reduced), reduced))

letters = list(map(chr, range(ord('a'), ord('z') + 1)))
minimum = len(polymer)
min_letter = None
for c in letters:
    removed = re.sub('[{}{}]'.format(c, c.upper()), '', polymer)
    reduced = react(removed)
    if minimum > len(reduced):
        minimum = len(reduced)
        min_letter = c
print("Part 2: Letter '{}' results in a reacted length of {}".format(min_letter, minimum))
