use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[derive(Clone, Debug)]
struct Step {
    name: char,
    prerequisites: Vec<char>,
}

impl Step {
    fn duration(&self) -> u16 {
        60 + self.name as u16 - 'A' as u16 + 1
    }
}

#[derive(Debug)]
struct Worker {
    step: Option<char>,
    free_in: u16,
}

impl Worker {
    #[rustfmt::skip]
    fn build_workers(count: u8) -> Vec<Worker> {
        (0..count).map(|_| Worker { step: None, free_in: 0 }).collect()
    }

    fn is_busy(&self) -> bool {
        self.step.is_some()
    }

    fn assign(&mut self, step: &Step) {
        self.step = Some(step.name);
        self.free_in = step.duration();
    }

    fn do_work(&mut self) -> Option<char> {
        self.free_in = self.free_in.saturating_sub(1);
        if self.free_in == 0 {
            let finished = self.step;
            self.step = None;
            return finished;
        }
        None
    }
}

fn parse_input() -> Result<HashMap<char, Step>, Box<Error>> {
    let buf_reader = BufReader::new(File::open("../inputs/07-input.txt")?);
    let mut steps = HashMap::new();
    for line in buf_reader.lines().flatten() {
        let mut chars = line.chars();
        let prereq = chars.nth(5).expect("error parsing prerequisite");
        let name = chars.nth(30).expect("error parsing step");
        steps.entry(prereq).or_insert(Step {
            name: prereq,
            prerequisites: vec![],
        });
        let entry = steps.entry(name).or_insert(Step {
            name,
            prerequisites: vec![],
        });
        entry.prerequisites.push(prereq);
    }
    Ok(steps)
}

fn next_steps(steps: &HashMap<char, Step>, completed: &[char], in_progress: &[char]) -> Vec<Step> {
    let mut next_steps: Vec<Step> = steps
        .values()
        .filter(|s| {
            !completed.contains(&s.name)
                && !in_progress.contains(&s.name)
                && s.prerequisites.iter().all(|p| completed.contains(p))
        })
        .cloned()
        .collect();
    next_steps.sort_unstable_by_key(|s| s.name);
    next_steps
}

pub fn part1() -> Result<String, Box<Error>> {
    let steps = parse_input()?;
    let mut completed = vec![];
    while let Some(next_step) = next_steps(&steps, &completed, &[]).first() {
        completed.push(next_step.name);
    }
    Ok(completed.iter().collect())
}

pub fn part2() -> Result<u16, Box<Error>> {
    let steps = parse_input()?;
    let mut seconds = 0;
    let mut completed = vec![];
    let mut in_progress = vec![];
    let mut workers = Worker::build_workers(5);
    while completed.len() < steps.len() {
        let next_steps = next_steps(&steps, &completed, &in_progress);
        let mut iter = next_steps.iter();
        while let (Some(next_step), Some(worker)) =
            (iter.next(), workers.iter_mut().find(|w| !w.is_busy()))
        {
            in_progress.push(next_step.name);
            worker.assign(next_step);
        }
        workers.iter_mut().for_each(|w| {
            if let Some(finished) = w.do_work() {
                completed.push(finished);
            }
        });
        seconds += 1;
    }
    Ok(seconds)
}
