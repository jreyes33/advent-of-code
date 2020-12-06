use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::Read;
use std::str::FromStr;

#[derive(Debug, Eq, Hash, PartialEq)]
struct Alive(Vec<bool>);

impl FromStr for Alive {
    type Err = Box<Error>;

    fn from_str(string: &str) -> Result<Alive, Box<Error>> {
        Ok(Alive(string.chars().map(|c| c == '#').collect()))
    }
}

#[derive(Debug)]
struct Plants {
    alive: Alive,
    start_idx: i64,
    rules: HashMap<Alive, bool>,
}

impl FromStr for Plants {
    type Err = Box<Error>;

    fn from_str(string: &str) -> Result<Plants, Box<Error>> {
        let mut lines = string.lines();
        let first_line = lines.next().ok_or("empty input")?;
        let alive = first_line
            .split(' ')
            .nth(2)
            .ok_or("failed reading plants")?
            .parse()?;
        let mut rules = HashMap::new();
        for line in lines.skip(1) {
            let mut split = line.split(' ');
            let rule = split.next().ok_or("failed reading rule")?.parse()?;
            let result = "#" == split.last().ok_or("failed reading rule result")?;
            rules.insert(rule, result);
        }
        Ok(Plants { alive, rules, start_idx: 0 })
    }
}

impl Plants {
    fn next_gen(&mut self) {
        let mut padded_alive = vec![false; 3];
        padded_alive.extend_from_slice(&self.alive.0);
        padded_alive.extend_from_slice(&[false; 3]);
        self.start_idx -= 1;
        let mut new_alive = vec![];
        for i in 2..padded_alive.len() - 2 {
            let rule = Alive(padded_alive[i - 2..i + 3].to_vec());
            let result = self.rules.get(&rule).unwrap_or(&false);
            new_alive.push(*result);
        }
        self.alive = Alive(new_alive);
    }

    fn sum_alive(&self) -> i64 {
        self.alive.0.iter().enumerate()
            .filter(|(_, &a)| a)
            .map(|(i, _)| i as i64 + self.start_idx)
            .sum()
    }
}

fn parse_input() -> Result<Plants, Box<Error>> {
    let mut contents = String::new();
    File::open("../inputs/12-input.txt")?.read_to_string(&mut contents)?;
    Ok(contents.parse()?)
}

pub fn part1() -> Result<i64, Box<Error>> {
    let mut plants = parse_input()?;
    for _ in 0..20 {
        plants.next_gen();
    }
    Ok(plants.sum_alive())
}

pub fn part2() -> Result<i64, Box<Error>> {
    let mut plants = parse_input()?;
    let mut i = 0;
    let mut sum_diff = 0;
    loop {
        i += 1;
        let last_sum = plants.sum_alive();
        plants.next_gen();
        let new_sum = plants.sum_alive();
        if sum_diff == new_sum - last_sum {
            break;
        }
        sum_diff = new_sum - last_sum;
    }
    let k = plants.sum_alive() - i * sum_diff;
    Ok(5e10 as i64 * sum_diff + k)
}
