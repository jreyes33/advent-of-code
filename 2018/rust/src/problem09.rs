use std::cell::RefCell;
use std::error::Error;
use std::fs::File;
use std::io::Read;
use std::rc::Rc;

struct Settings(usize, u32);

struct Circle {
    current: Rc<RefCell<Marble>>,
    first: Rc<RefCell<Marble>>,
    last: Rc<RefCell<Marble>>,
}

impl Circle {
    fn new(value: u32) -> Circle {
        let current = Rc::new(RefCell::new(Marble { value, next: None, prev: None }));
        let first = Rc::clone(&current);
        let last = Rc::clone(&current);
        Circle { current, first, last }
    }

    fn backward(&mut self, steps: u32) {
        for _i in 0..steps {
            let current_ref = Rc::clone(&self.current);
            let current = current_ref.borrow();
            match current.prev {
                None => self.current = Rc::clone(&self.last),
                Some(ref marble) => self.current = Rc::clone(marble),
            }
        }
    }

    fn forward(&mut self, steps: u32) {
        for _i in 0..steps {
            let current_ref = Rc::clone(&self.current);
            let current = current_ref.borrow();
            match current.next {
                None => self.current = Rc::clone(&self.first),
                Some(ref marble) => self.current = Rc::clone(marble),
            }
        }
    }

    fn insert_after_current(&mut self, value: u32) {
        let current_ref = Rc::clone(&self.current);
        let mut current = current_ref.borrow_mut();
        let inserted = Rc::new(RefCell::new(Marble { value, next: None, prev: None }));
        match current.next {
            None => self.last = Rc::clone(&inserted),
            Some(ref marble) => {
                inserted.borrow_mut().next = Some(Rc::clone(marble));
                marble.borrow_mut().prev = Some(Rc::clone(&inserted));
            }
        }
        inserted.borrow_mut().prev = Some(Rc::clone(&current_ref));
        current.next = Some(Rc::clone(&inserted));
        self.current = Rc::clone(&inserted);
    }

    fn remove_current(&mut self) -> u32 {
        let removed_ref = Rc::clone(&self.current);
        let removed = removed_ref.borrow();
        match removed.prev {
            None => self.first = Rc::clone(removed.next.as_ref().unwrap()),
            Some(ref prev) => {
                prev.borrow_mut().next = Some(Rc::clone(removed.next.as_ref().unwrap()))
            }
        }
        match removed.next {
            None => {
                self.last = Rc::clone(removed.prev.as_ref().unwrap());
                self.current = Rc::clone(&self.first);
            }
            Some(ref next) => {
                next.borrow_mut().prev = Some(Rc::clone(removed.prev.as_ref().unwrap()));
                self.current = Rc::clone(&next);
            }
        }
        removed.value
    }
}

struct Marble {
    value: u32,
    next: Option<Rc<RefCell<Marble>>>,
    prev: Option<Rc<RefCell<Marble>>>,
}

fn parse_input() -> Result<Settings, Box<Error>> {
    let mut contents = String::new();
    File::open("../inputs/09-input.txt")?.read_to_string(&mut contents)?;
    let mut split = contents.split(' ');
    let player_count = split.nth(0).ok_or("failed parsing players")?.parse()?;
    let last_marble = split.nth(5).ok_or("failed parsing last marble")?.parse()?;
    Ok(Settings(player_count, last_marble))
}

fn _naive_vector_solution(settings: &Settings) -> Result<u32, Box<Error>> {
    let Settings(player_count, last_marble) = *settings;
    let mut marbles = vec![0u32];
    let mut scores = vec![0u32; player_count];
    let mut current_idx = 0;
    let mut scores_idx = 0;
    for marble in 1..=last_marble {
        let length = marbles.len();
        if marble % 23 == 0 {
            if 7 > current_idx {
                current_idx = length - (7 - current_idx);
            } else {
                current_idx -= 7;
            }
            let removed = marbles.remove(current_idx);
            scores[scores_idx] += marble + removed;
        } else {
            current_idx = (current_idx + 2) % length;
            marbles.insert(current_idx, marble);
        }
        scores_idx = (scores_idx + 1) % player_count;
    }
    Ok(*scores.iter().max().ok_or("failed getting max score")?)
}

fn performant_linked_list_solution(settings: &Settings) -> Result<u32, Box<Error>> {
    let Settings(player_count, last_marble) = *settings;
    let mut scores = vec![0u32; player_count];
    let mut scores_idx = 0;
    let mut circle = Circle::new(0);
    for marble in 1..=last_marble {
        if marble % 23 == 0 {
            circle.backward(7);
            scores[scores_idx] += marble + circle.remove_current();
        } else {
            circle.forward(1);
            circle.insert_after_current(marble);
        }
        scores_idx = (scores_idx + 1) % player_count;
    }
    Ok(*scores.iter().max().ok_or("failed getting max score")?)
}

pub fn part1() -> Result<u32, Box<Error>> {
    let settings = parse_input()?;
    performant_linked_list_solution(&settings)
}


pub fn part2() -> Result<u32, Box<Error>> {
    let Settings(player_count, last_marble) = parse_input()?;
    performant_linked_list_solution(&Settings(player_count, last_marble * 100))
}
