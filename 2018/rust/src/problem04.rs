use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::ops::Range;

#[derive(Debug)]
struct SleepTime {
    month: u8,
    day: u8,
    range: Range<u32>,
}

#[derive(Debug)]
struct Guard {
    id: u32,
    sleep_times: Vec<SleepTime>,
}

impl Guard {
    fn minutes_asleep(&self) -> u32 {
        self.sleep_times
            .iter()
            .fold(0, |acc, x| acc + x.range.end - x.range.start)
    }

    fn times_asleep_at(&self, minute: u32) -> u32 {
        self.sleep_times
            .iter()
            .filter(|x| x.range.start <= minute && minute < x.range.end)
            .count() as u32
    }
}

type SleepRecords = HashMap<u32, Guard>;

fn parse_input() -> Result<SleepRecords, Box<Error>> {
    let buf_reader = BufReader::new(File::open("../inputs/04-input.txt")?);
    let mut lines: Vec<_> = buf_reader.lines().flatten().collect();
    lines.sort();
    let mut id = 0;
    let mut sleep_records = HashMap::new();
    for line in &lines {
        if line.ends_with("begins shift") {
            id = line.split(' ').nth(3).ok_or("error reading id")?[1..].parse()?;
        } else if line.ends_with("falls asleep") {
            let guard = sleep_records.entry(id).or_insert(Guard {
                id,
                sleep_times: vec![],
            });
            let minute = line[15..17].parse()?;
            let sleep_time = SleepTime {
                month: line[6..8].parse()?,
                day: line[9..11].parse()?,
                range: minute..59,
            };
            guard.sleep_times.push(sleep_time);
        } else if line.ends_with("wakes up") {
            let guard = sleep_records.get_mut(&id).ok_or("no current guard")?;
            let minute = line[15..17].parse()?;
            let sleep_time = guard.sleep_times.last_mut().ok_or("guard was not asleep")?;
            sleep_time.range.end = minute;
        }
    }
    Ok(sleep_records)
}

pub fn part1() -> Result<u32, Box<Error>> {
    let sleep_records = parse_input()?;
    let sleepy = sleep_records
        .values()
        .max_by_key(|x| x.minutes_asleep())
        .ok_or("could not find the sleepiest guard")?;
    let minute = (0..=59)
        .max_by_key(|&x| sleepy.times_asleep_at(x))
        .ok_or("could not find the sleepiest minute")?;
    Ok(sleepy.id * minute)
}

pub fn part2() -> Result<u32, Box<Error>> {
    let sleep_records = parse_input()?;
    let mut minute = 0;
    let mut max_times_asleep_at_minute = 0;
    let mut sleepy = None;
    for i in 0..=59 {
        for guard in sleep_records.values() {
            let times = guard.times_asleep_at(i);
            if times > max_times_asleep_at_minute {
                max_times_asleep_at_minute = times;
                minute = i;
                sleepy = Some(guard);
            }
        }
    }
    let id = sleepy.ok_or("could not find the sleepiest guard")?.id as u32;
    Ok(id * minute)
}
