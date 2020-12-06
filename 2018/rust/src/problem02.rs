use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

fn parse_input() -> Result<Vec<String>, Box<Error>> {
    let buf_reader = BufReader::new(File::open("../inputs/02-input.txt")?);
    let lines = buf_reader.lines().flatten().collect();
    Ok(lines)
}

pub fn part1() -> Result<i32, Box<Error>> {
    let mut has_2_count = 0;
    let mut has_3_count = 0;
    for line in parse_input()? {
        let mut letters_count = HashMap::new();
        for letter in line.chars() {
            let count = letters_count.entry(letter).or_insert(0);
            *count += 1;
        }
        if letters_count.iter().any(|(_, &count)| count == 2) {
            has_2_count += 1
        }
        if letters_count.iter().any(|(_, &count)| count == 3) {
            has_3_count += 1
        }
    }
    Ok(has_2_count * has_3_count)
}

pub fn part2() -> Result<(String, String), Box<Error>> {
    let lines = parse_input()?;
    let lines_copy = lines.clone();
    for line in lines {
        for other in lines_copy.clone() {
            let distance = line
                .chars()
                .zip(other.chars())
                .filter(|(a, b)| a != b)
                .count();
            if distance == 1 {
                return Ok((line, other));
            }
        }
    }
    Err(From::from("none found"))
}
