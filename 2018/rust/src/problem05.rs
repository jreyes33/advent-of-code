use std::error::Error;
use std::fs::File;
use std::io::prelude::*;

type Polymer = Vec<char>;

fn parse_input() -> Result<Polymer, Box<Error>> {
    let mut contents = String::new();
    File::open("../inputs/05-input.txt")?.read_to_string(&mut contents)?;
    Ok(contents.trim().chars().collect())
}

fn react(polymer_arg: Polymer) -> Polymer {
    let mut i = 0;
    let mut polymer = polymer_arg;
    let mut result = vec![];
    loop {
        let j = i + 1;
        let unit = polymer[i];
        if j >= polymer.len() {
            result.push(unit);
            return result;
        }
        let next_unit = polymer[j];
        let correct_cases = unit.is_lowercase() && next_unit.is_uppercase()
            || unit.is_uppercase() && next_unit.is_lowercase();
        let same_letter = unit.to_lowercase().next() == next_unit.to_lowercase().next();
        if correct_cases && same_letter {
            result.pop();
            polymer.remove(i);
            polymer.remove(i);
            i = i.saturating_sub(1);
        } else {
            result.push(unit);
            i += 1;
        }
    }
}

pub fn part1() -> Result<usize, Box<Error>> {
    let polymer = parse_input()?;
    Ok(react(polymer).len())
}

pub fn part2() -> Result<usize, Box<Error>> {
    let polymer = parse_input()?;
    let mut min_len = polymer.len();
    for unit in (b'a'..=b'z').map(char::from) {
        let mut clean_polymer = polymer.clone();
        clean_polymer.retain(|u| unit != u.to_lowercase().next().expect("should be lowercasable"));
        let len = react(clean_polymer).len();
        if len < min_len {
            min_len = len;
        }
    }
    Ok(min_len)
}
