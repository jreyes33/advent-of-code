package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

type Square struct {
	x, y, size, power int
}

type Grid [300][300]int

func NewGrid(serial int) *Grid {
	grid := new(Grid)
	for i, row := range grid {
		for j, _ := range row {
			rackId := j + 11
			powerLevel := (rackId * (i + 1) + serial) * rackId
			summedArea := (powerLevel / 100) % 10 - 5
			// https://en.wikipedia.org/wiki/Summed-area_table
			if i > 0 {
				summedArea += grid[i-1][j]
			}
			if j > 0 {
				summedArea += grid[i][j-1]
			}
			if i > 0 && j > 0 {
				summedArea -= grid[i-1][j-1]
			}
			grid[i][j] = summedArea
		}
	}
	return grid
}

func (grid *Grid) squarePower(x, y, size int) int {
	oppX := x + size - 1
	oppY := y + size - 1
	power := grid[oppY][oppX]
	if x > 0 {
		power -= grid[oppY][x - 1]
	}
	if y > 0 {
		power -= grid[y - 1][oppX]
	}
	if x > 0 && y > 0 {
		power += grid[y - 1][x - 1]
	}
	return power
}

func (grid *Grid) maxSquare(minSize, maxSize int) *Square {
	maxSquare := Square{0, 0, 0, 0}
	for size := minSize; size <= maxSize; size++ {
		for i := 0; i <= 300 - size; i++ {
			for j := 0; j <= 300 - size; j++ {
				power := grid.squarePower(j, i, size)
				if power > maxSquare.power {
					maxSquare = Square{j, i, size, power}
				}
			}
		}
	}
	return &maxSquare
}

func parseInput() int {
	input, err := ioutil.ReadFile("../inputs/11-input.txt")
	if err != nil {
		log.Fatal(err)
	}
	serial, err := strconv.Atoi(strings.TrimSpace(string(input)))
	if err != nil {
		log.Fatal(err)
	}
	return serial
}

func main() {
	grid := NewGrid(parseInput())
	maxSquare1 := grid.maxSquare(3, 3)
	fmt.Printf("Part1: %v,%v\n", maxSquare1.x+1, maxSquare1.y+1)
	maxSquare2 := grid.maxSquare(1, 300)
	fmt.Printf("Part2: %v,%v,%v\n", maxSquare2.x+1, maxSquare2.y+1, maxSquare2.size)
}
