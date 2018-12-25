fs = require('fs')

fs.readFile('input.txt', 'utf8', function(err, contents) {
    var sorted = contents.split('\n')
        .sort()
        .filter(x => x.length > 0);
    console.log(sorted);
    var guards = {};
    var currentId;
    var currentSleep;
    sorted.forEach(line => {
        var day = Number(line.split(" ")[0].split("-")[2]);
        var minute = Number(line.slice(15, 17));
        if(line.includes("begins shift")) {
            currentId = Number(line.split("#")[1].split(" ")[0]);
            if(guards[currentId] == null) {
                guards[currentId] = [];
            }
        }
        else if(line.includes("falls asleep")) {
            currentSleep = {"day": day, "sleepStart": minute};
        }
        else if(line.includes("wakes up")) {
            currentSleep["sleepEnd"] = minute;
            guards[currentId].push(currentSleep);
        }
    });
    console.log(guards);
    var longestAsleep = { "duration" : 0 };
    var mostFrequentAsleep = { "frequency" : 0 };
    for(var id in guards) {
        var diffs = guards[id]
            .map(period => period["sleepEnd"] - period["sleepStart"]);
        var totalMinutes = diffs.length == 0 ? 0 : diffs
            .reduce((a, b) => a + b);
        if(totalMinutes > longestAsleep["duration"]) {
            longestAsleep["duration"] = totalMinutes;
            longestAsleep["id"] = id;
        }
        // Part 2
        var minute = magicMinute(guards[id]);
        if(minute["frequency"] > mostFrequentAsleep["frequency"]) {
            mostFrequentAsleep["frequency"] = minute["frequency"];
            mostFrequentAsleep["minute"] = minute["minute"];
            mostFrequentAsleep["id"] = id;
        }
    }
    var minute = magicMinute(guards[longestAsleep["id"]])["minute"];
    console.log("Magic minute: %d", minute);
    console.log("Longest asleep %d minutes, id: %d",
        longestAsleep["duration"],
        longestAsleep["id"]);
    console.log("Part 1 answer %d * %d = %d",
        longestAsleep["id"],
        minute,
        longestAsleep["id"] * minute);

    console.log("Part 2 answer %d * %d = %d",
        mostFrequentAsleep["id"],
        mostFrequentAsleep["minute"],
        mostFrequentAsleep["id"] * mostFrequentAsleep["minute"])
});

function magicMinute(periods) {
    var heatmap = [];
    for(var i = 0; i < 60; ++i) {
        heatmap[i] = 0;
    }
    periods.forEach(period => {
        for(var i = period["sleepStart"]; i < period["sleepEnd"]; ++i) {
            heatmap[i] += 1;
        }
    });
    var magicMinute = 0;
    var magicHeat = 0;
    for(var i = 0; i < heatmap.length; ++i) {
        if(heatmap[i] > magicHeat) {
            magicHeat = heatmap[i];
            magicMinute = i;
        }
    }
    return {
        "minute": magicMinute,
        "frequency": magicHeat
    };
}
