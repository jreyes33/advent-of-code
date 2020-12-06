use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;

#[derive(Debug)]
struct Point(i16, i16);

impl Point {
    fn closest(&self, points: &[Point]) -> Option<usize> {
        let mut min_distance = std::i16::MAX;
        let mut closest_idx = None;
        for (i, p) in points.iter().enumerate() {
            let distance_to_p = self.distance(p);
            if distance_to_p < min_distance {
                min_distance = distance_to_p;
                closest_idx = Some(i);
            } else if distance_to_p == min_distance {
                closest_idx = None;
            }
        }
        closest_idx
    }

    fn distance(&self, other: &Point) -> i16 {
        (other.0 - self.0).abs() + (other.1 - self.1).abs()
    }

    fn total_distance(&self, points: &[Point]) -> i16 {
        points.iter().map(|p| self.distance(p)).sum()
    }
}

fn parse_input() -> Result<Vec<Point>, Box<Error>> {
    let buf_reader = BufReader::new(File::open("../inputs/06-input.txt")?);
    let lines: Vec<_> = buf_reader.lines().flatten().collect();
    let mut points = vec![];
    for line in lines {
        let mut split = line.split(',');
        let x = split.next().ok_or("failed parsing x")?.parse()?;
        let y = split.next().ok_or("failed parsing y")?.trim().parse()?;
        points.push(Point(x, y));
    }
    Ok(points)
}

#[rustfmt::skip]
fn boundaries(points: &[Point]) -> (Point, Point) {
    let min_x = points.iter().min_by_key(|p| p.0).expect("points is empty").0;
    let min_y = points.iter().min_by_key(|p| p.1).expect("points is empty").1;
    let max_x = points.iter().max_by_key(|p| p.0).expect("points is empty").0;
    let max_y = points.iter().max_by_key(|p| p.1).expect("points is empty").1;
    (Point(min_x, min_y), Point(max_x, max_y))
}

pub fn part1() -> Result<u16, Box<Error>> {
    let points = parse_input()?;
    let (Point(min_x, min_y), Point(max_x, max_y)) = boundaries(&points);
    let mut closest_points = vec![];
    let mut infinite_areas = HashSet::new();
    for j in min_y..=max_y {
        for i in min_x..=max_x {
            let closest = Point(i, j).closest(&points);
            closest_points.push(closest);
            if i == min_x || i == max_x || j == min_y || j == max_y {
                infinite_areas.insert(closest);
            }
        }
    }
    let mut counts = HashMap::new();
    for p in closest_points
        .iter()
        .filter(|p| p.is_some() && !infinite_areas.contains(p))
    {
        let idx = p.expect("already filtered out nones");
        let entry = counts.entry(idx).or_insert(0);
        *entry += 1;
    }
    let result = counts.values().max().expect("all areas were infinite");
    Ok(*result)
}

pub fn part2() -> Result<usize, Box<Error>> {
    let points = parse_input()?;
    let (Point(min_x, min_y), Point(max_x, max_y)) = boundaries(&points);
    let mut total_distances = vec![];
    for j in min_y..=max_y {
        for i in min_x..=max_x {
            total_distances.push(Point(i, j).total_distance(&points));
        }
    }
    let result = total_distances.iter().filter(|&&d| d < 10000).count();
    Ok(result)
}
