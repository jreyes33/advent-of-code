package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

const MAX_X = 80
const MAX_Y = 24
const RESET_CURSOR = "\033[H"
const CLEAR_SCREEN = "\033[2J"

type Point struct {
	x, y int
}

type Light struct {
	position, velocity Point
}

type Sky [][]bool

func NewSky(sizeX, sizeY int) *Sky {
	var sky Sky
	for i := 0; i < sizeY; i++ {
		var row []bool
		for j := 0; j < sizeX; j++ {
			row = append(row, false)
		}
		sky = append(sky, row)
	}
	return &sky
}

func (sky *Sky) String() string {
	var builder strings.Builder
	for _, row := range *sky {
		for _, lightOn := range row {
			if lightOn {
				builder.WriteRune('·')
			} else {
				builder.WriteRune(' ')
			}
		}
		builder.WriteRune('\n')
	}
	return builder.String()
}

func (sky *Sky) clean() {
	for i, row := range *sky {
		for j := range row {
			(*sky)[i][j] = false
		}
	}
}

func convert(text *string) int {
	number, err := strconv.Atoi(strings.TrimSpace(*text))
	if err != nil {
		log.Fatal(err)
	}
	return number
}

func parseInput() []Light {
	file, err := os.Open("../inputs/10-input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var lights []Light
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), ">")
		positionInput := strings.Split(parts[0], "<")[1]
		velocityInput := strings.Split(parts[1], "<")[1]
		positionParts := strings.Split(positionInput, ",")
		velocityParts := strings.Split(velocityInput, ",")
		position := Point{convert(&positionParts[0]), convert(&positionParts[1])}
		velocity := Point{convert(&velocityParts[0]), convert(&velocityParts[1])}
		lights = append(lights, Light{position, velocity})
	}
	return lights
}

func main() {
	lights := parseInput()
	lightsCount := len(lights)
	sky := NewSky(MAX_X, MAX_Y)
	seconds := 0
	maxVisible := 0
	for {
		sky.clean()
		seconds += 1
		lightsVisible := 0
		topLeft := Point{1e6, 1e6}
		for i, light := range lights {
			light.position.x += light.velocity.x
			light.position.y += light.velocity.y
			lights[i] = light
			if light.position.x <= topLeft.x && light.position.y <= topLeft.y {
				topLeft = light.position
			}
		}

		for _, light := range lights {
			x := light.position.x
			y := light.position.y
			if x >= topLeft.x && x < MAX_X+topLeft.x && y >= topLeft.y && y < MAX_Y+topLeft.y {
				(*sky)[y-topLeft.y][x-topLeft.x] = true
				lightsVisible += 1
			}
		}

		if lightsVisible >= maxVisible {
			maxVisible = lightsVisible
			if lightsVisible > lightsCount/25 {
				fmt.Printf("%v%v%v\nSeconds: %v\n", CLEAR_SCREEN, RESET_CURSOR, sky, seconds)
				time.Sleep(150 * time.Millisecond)
			}
		}
	}
}
