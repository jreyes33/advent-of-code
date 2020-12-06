use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[derive(Clone, Debug)]
struct Point(u16, u16);

#[derive(Clone, Debug)]
struct Claim {
    id: u16,
    corner: Point,
    size: Point,
}

impl Claim {
    fn limit(&self) -> Point {
        Point(self.corner.0 + self.size.0, self.corner.1 + self.size.1)
    }

    fn contains(&self, point: &Point) -> bool {
        let contains_x = self.corner.0 <= point.0 && point.0 < self.limit().0;
        let contains_y = self.corner.1 <= point.1 && point.1 < self.limit().1;
        contains_x && contains_y
    }
}

fn more_than_x_claims(max: u16, point: &Point, claims: &[Claim]) -> bool {
    let mut count = 0;
    for claim in claims {
        if claim.contains(&point) {
            count += 1;
        }
        if count >= max {
            return true;
        }
    }
    false
}

fn parse_input() -> Result<Vec<Claim>, Box<Error>> {
    let buf_reader = BufReader::new(File::open("../inputs/03-input.txt")?);
    let lines: Vec<_> = buf_reader.lines().flatten().collect();
    let mut claims = vec![];
    for line in lines {
        let mut split = line.split(' ');
        let id_input = split.next().ok_or("error reading id")?;
        let corner_input = split.nth(1).ok_or("error reading corner coords")?;
        let size_input = split.next().ok_or("error reading size")?;
        let mut corner_split = corner_input[..corner_input.len() - 1].split(',');
        let mut size_split = size_input.split('x');
        let corner_x = corner_split.next().ok_or("corner_x failed")?.parse()?;
        let corner_y = corner_split.next().ok_or("corner_y failed")?.parse()?;
        let size_x = size_split.next().ok_or("size_x failed")?.parse()?;
        let size_y = size_split.next().ok_or("size_y failed")?.parse()?;
        let id = id_input[1..].parse()?;
        let corner = Point(corner_x, corner_y);
        let size = Point(size_x, size_y);
        claims.push(Claim { id, corner, size });
    }
    Ok(claims)
}

pub fn part1() -> Result<u32, Box<Error>> {
    let claims = parse_input()?;
    let mut overlapping = 0;
    for i in 0..1000 {
        for j in 0..1000 {
            if more_than_x_claims(2, &Point(i, j), &claims) {
                overlapping += 1;
            }
        }
    }
    Ok(overlapping)
}

pub fn part2() -> Result<u16, Box<Error>> {
    let claims = parse_input()?;
    for claim in claims.clone() {
        let mut the_chosen_one = true;
        for i in claim.corner.0..claim.limit().0 {
            for j in claim.corner.1..claim.limit().1 {
                if more_than_x_claims(2, &Point(i, j), &claims) {
                    the_chosen_one = false;
                }
            }
        }
        if the_chosen_one {
            return Ok(claim.id);
        }
    }
    Err(From::from("could not find claim not overlapping"))
}
