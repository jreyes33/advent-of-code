use std::collections::HashSet;
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

fn parse_input() -> Result<Vec<i32>, Box<Error>> {
    let buf_reader = BufReader::new(File::open("../inputs/01-input.txt")?);
    // Commented this out because of ugly double unwrap
    // let numbers = buf_reader
    //     .lines()
    //     .map(|line| line.unwrap().parse().unwrap())
    //     .collect();
    let mut numbers = vec![];
    for line in buf_reader.lines() {
        numbers.push(line?.parse()?);
    }
    Ok(numbers)
}

pub fn part1() -> Result<i32, Box<Error>> {
    let result = parse_input()?.iter().sum();
    Ok(result)
}

pub fn part2() -> Result<i32, Box<Error>> {
    let mut result = 0;
    let mut results = HashSet::new();
    results.insert(result);
    let numbers = parse_input()?;
    for n in numbers.iter().cycle() {
        result += n;
        if results.contains(&result) {
            break;
        }
        results.insert(result);
    }
    Ok(result)
}
