use std::env;
use std::error::Error;
use std::process;

mod problem01;
mod problem02;
mod problem03;
mod problem04;
mod problem05;
mod problem06;
mod problem07;
mod problem08;
mod problem09;
mod problem12;

fn main() -> Result<(), Box<Error>> {
    let problem: u8 = env::args()
        .nth(1)
        .ok_or("Please provide a problem number")?
        .parse()?;
    match problem {
        1 => {
            println!("{}", problem01::part1()?);
            println!("{}", problem01::part2()?);
        }
        2 => {
            println!("{}", problem02::part1()?);
            println!("{:?}", problem02::part2()?);
        }
        3 => {
            println!("{}", problem03::part1()?);
            println!("{}", problem03::part2()?);
        }
        4 => {
            println!("{}", problem04::part1()?);
            println!("{}", problem04::part2()?);
        }
        5 => {
            println!("{}", problem05::part1()?);
            println!("{}", problem05::part2()?);
        }
        6 => {
            println!("{}", problem06::part1()?);
            println!("{}", problem06::part2()?);
        }
        7 => {
            println!("{}", problem07::part1()?);
            println!("{}", problem07::part2()?);
        }
        8 => {
            println!("{}", problem08::part1()?);
            println!("{}", problem08::part2()?);
        }
        9 => {
            println!("{}", problem09::part1()?);
            println!("{}", problem09::part2()?);
        }
        12 => {
            println!("{}", problem12::part1()?);
            println!("{}", problem12::part2()?);
        }
        _ => {
            println!("No such problem: {}", problem);
            process::exit(1);
        }
    }
    Ok(())
}
