fs = require('fs')

var lineReader = require('readline').createInterface({
  input: require('fs').createReadStream('input.txt')
});

var fabric = [1000 * 1000];
var collisionCount = 0;
var nonOverlapping = new Set();
lineReader.on('line', function (line) {
    coords = line.split('@')[1].split(':')[0].split(',');
    size = line.split('@')[1].split(':')[1].split('x');
    id = line.slice(line.indexOf('#') + 1, line.indexOf('@'));
    square = {
      'id': Number(id),
      'x': Number(coords[0]),
      'y': Number(coords[1]),
      'w': Number(size[0]),
      'h': Number(size[1])
    }
    nonOverlapping.add(square.id);
    for(var y = square.y; y < square.y + square.h; ++y) {
        for(var x = square.x; x < square.x + square.w; ++x) {
            var inch = y * 1000 + x;
            if(typeof fabric[inch] === 'undefined') {
                fabric[inch] = []
            }
            fabric[inch].push(square.id);
            if(fabric[inch].length == 2) {
                collisionCount += 1;
            }
            if(fabric[inch].length > 1) {
                for(let id of fabric[inch]) {
                    nonOverlapping.delete(id);
                }
            }
        }
    }
}).on('close', function () {
    console.log("Part 1: number of collisions %d", collisionCount);
    console.log("Part 2: non-overlapping ids:");
    nonOverlapping.forEach(name => console.log(name));
});
