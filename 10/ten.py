with open('input.txt', 'r') as file:
    data = file.read()

max_time = 30000
close_box_x = 70
close_box_y = 15

def directions(input):
    result = []
    for line in input.strip().split('\n'):
        parts = line.split(',')
        px = int(parts[0].split('<')[1])
        py = int(parts[1].split('>')[0])
        vx = int(parts[1].split('<')[1])
        vy = int(parts[2].split('>')[0])
        result.append({
            'pos': (px, py),
            'velocity': (vx, vy)
        })
    return result


def update(dirs, time):
    return [(
        dir['pos'][0] + dir['velocity'][0] * time,
        dir['pos'][1] + dir['velocity'][1] * time
    ) for dir in dirs]


def print_sky(positions, box):
    xoffset = box[0]
    yoffset = box[2]
    width = box[1] - xoffset
    height = box[3] - yoffset
    sky = [[] for _ in range(height + 1)]
    for p in positions:
        x = p[0] - xoffset
        y = p[1] - yoffset
        if 0 <= x <= width and 0 <= y <= height:
            row = sky[y]
            if len(row) > x:
                row[x] = '#'
            else:
                row += ' ' * (x - len(row))
                row.append('#')
        else:
            print("Index out of range {}, {}".format(x, y))
    print('\n'.join([''.join([item for item in row])
                     for row in sky]))


def close_box(positions, time):
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)
    if maxx - minx < close_box_x and maxy - miny < close_box_y:
        print("Close box for time {}".format(time))
        return minx, maxx, miny, maxy
    return None


dirs = directions(data)
for time in range(1, max_time):
    positions = update(dirs, time)
    box = close_box(positions, time)
    if box is not None:
        print_sky(positions, box)


