use std::error::Error;
use std::fs::File;
use std::io::prelude::*;

#[derive(Debug)]
struct Node {
    children: Vec<Node>,
    metadata: Vec<u16>,
}

impl Node {
    #[rustfmt::skip]
    fn new() -> Node {
        Node { children: vec![], metadata: vec![] }
    }

    fn sum_metadata(&self) -> u16 {
        self.sum_own() + self.children.iter().map(|c| c.sum_metadata()).sum::<u16>()
    }

    fn sum_own(&self) -> u16 {
        self.metadata.iter().sum()
    }

    fn node_value(&self) -> u16 {
        if self.children.is_empty() {
            return self.sum_own();
        }
        self.metadata.iter().map(|&m| {
            let m_usize = m as usize;
            if m_usize > self.children.len() {
                return 0;
            }
            self.children[m_usize - 1].node_value()
        }).sum()
    }
}

fn parse_input() -> Result<Node, Box<Error>> {
    let mut contents = String::new();
    File::open("../inputs/08-input.txt")?.read_to_string(&mut contents)?;
    let mut input_iter = contents
        .trim()
        .split(' ')
        .map(|s| s.parse().expect("input must be parseable as numbers"));
    let mut children_pending: Vec<u16> = vec![];
    let mut metadata_pending: Vec<u16> = vec![];
    let mut nodes = vec![];
    while let Some(children_count) = input_iter.next() {
        let metadata_count = input_iter.next().ok_or("input interrupted (metadata_count)")?;
        children_pending.push(children_count);
        metadata_pending.push(metadata_count);
        nodes.push(Node::new());
        loop {
            let last_children_count = children_pending.pop().ok_or("children_pending empty")?;
            if last_children_count > 0 {
                children_pending.push(last_children_count);
                break;
            }
            let mut node = nodes.pop().ok_or("nodes empty")?;
            let last_metadata_count = metadata_pending.pop().ok_or("metadata_pending empty")?;
            for _i in 0..last_metadata_count {
                node.metadata.push(input_iter.next().ok_or("input interrupted (metadata)")?);
            }
            let mut parent = match nodes.pop() {
                Some(parent) => parent,
                None => {
                    nodes.push(node);
                    break;
                }
            };
            parent.children.push(node);
            nodes.push(parent);
            let new_children_count = children_pending.pop().ok_or("children_pending empty")? - 1;
            children_pending.push(new_children_count);
        }
    }
    Ok(nodes.pop().ok_or("root node parsing failed")?)
}

pub fn part1() -> Result<u16, Box<Error>> {
    let root_node = parse_input()?;
    Ok(root_node.sum_metadata())
}

pub fn part2() -> Result<u16, Box<Error>> {
    let root_node = parse_input()?;
    Ok(root_node.node_value())
}
