package main

import (
    "fmt"
    "io/ioutil"
    "strings"
    "strconv"
)

func parse(input string) []int {
    var split = strings.Split(input, "\n")
    //numbers := make([]int, len(split))
    var numbers []int
    for _, n := range split {
        if len(n) > 0 {
            var parsed, error = strconv.Atoi(n)
            if error != nil {
                panic(fmt.Sprintf("Parse error for '%s':%s", n, error))
            }
            numbers = append(numbers, parsed)
        }
    }
    return numbers
}

func sum(numbers []int) int {
    var result = 0
    for _, n := range numbers {
        result += n
    }
    return result
}

func firstTwice(numbers []int) int {
    var result = 0
    var frequencies = map[int]bool{ result: true }
    for true {  // Oh yeah! \o/
        for _, n := range numbers {
            result += n
            if _, ok := frequencies[result]; ok {
                return result
            }
            frequencies[result] = true
        }
    }
    return -1
}

func main() {
    data, error := ioutil.ReadFile("input.txt")
    if error != nil {
        panic("Oh noes")
    }
    var numbers = parse(string(data))
    fmt.Printf("Sum: %d\n", sum(numbers))
    fmt.Printf("First twice frequence: %d\n", firstTwice(numbers))
}
