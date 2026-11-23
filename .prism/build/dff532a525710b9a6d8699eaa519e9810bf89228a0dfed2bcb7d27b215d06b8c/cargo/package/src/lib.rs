#![cfg_attr(not(feature = "std"), no_std)]
#![allow(dead_code, non_snake_case, unused_parens, unused_variables)]
extern crate alloc;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ComputeError {
    AddOverflow,
    MulOverflow,
    ShiftExponentTooLarge,
    ShiftOverflow,
    PowExponentTooLarge,
    PowOverflow,
    OutputTooSmall,
}

pub fn appendBytes(left: alloc::vec::Vec<u8>, right: alloc::vec::Vec<u8>) -> alloc::vec::Vec<u8> {
    { let _x_2 = { let mut __append = (left, right); __append.0.extend(__append.1); __append.0 }; _x_2 }
}

pub fn byteLength(value: alloc::vec::Vec<u8>) -> u64 {
    __prod_borrowed_byteLength(value.as_ref())
}

fn __prod_borrowed_byteLength(value: &[u8]) -> u64 {
    { let _x_2 = (value).len() as u64; _x_2 }
}

pub fn decode(value: alloc::vec::Vec<u8>) -> Option<alloc::string::String> {
    { let _x_1 = alloc::string::String::from_utf8(value).ok(); _x_1 }
}

pub fn dispatch(value: alloc::vec::Vec<u8>) -> alloc::vec::Vec<u8> {
    { let _x_128 = (value).len() as u64; { let _x_2 = 0; { let _x_5 = (_x_128 == _x_2); match _x_5 {
        false => { let _x_392 = 64; { let _x_393 = (_x_392 < _x_128); match _x_393 {
        false => { let _x_452 = alloc::string::String::from_utf8(value.clone()).ok(); match _x_452 {
        None => alloc::vec![105, 110, 118, 97, 108, 105, 100],
        Some(val_469) => { let _x_491 = { let mut __value = alloc::vec![65, 99, 99, 101, 112, 116, 101, 100, 58, 32]; __value.extend_from_slice(&value); __value }; _x_491 },
    } },
        true => alloc::vec![105, 110, 118, 97, 108, 105, 100],
    } } },
        true => alloc::vec![105, 110, 118, 97, 108, 105, 100],
    } } } }
}
