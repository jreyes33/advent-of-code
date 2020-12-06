use std::error::Error;

pub mod intcode;

pub type Result<T> = std::result::Result<T, Box<dyn Error>>;
