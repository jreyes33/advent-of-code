package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

func parseInput() []int {
	file, err := os.Open("../inputs/01-input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var numbers []int
	for scanner.Scan() {
		number, err := strconv.Atoi(scanner.Text())
		if err != nil {
			log.Fatal(err)
		}
		numbers = append(numbers, number)
	}
	return numbers
}

func part1() int {
	numbers := parseInput()
	result := 0
	for _, v := range numbers {
		result += v
	}
	return result
}

func part2() int {
	numbers := parseInput()
	result := 0
	results := map[int]bool{0: true}
	for i := 0; ; i = (i + 1) % len(numbers) {
		result += numbers[i]
		_, has_result := results[result]
		if has_result {
			return result
		}
		results[result] = true
	}
}

func main() {
	fmt.Println(part1())
	fmt.Println(part2())
}
