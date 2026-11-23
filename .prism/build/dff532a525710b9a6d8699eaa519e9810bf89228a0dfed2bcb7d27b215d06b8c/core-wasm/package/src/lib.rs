#![no_std]
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



mod __prod_core_wasm_runtime {
use core::alloc::{GlobalAlloc, Layout};
use core::sync::atomic::{AtomicU32, Ordering};

const INPUT_CAP: u32 = 128;
const OUTPUT_CAP: u32 = 256;
const MAXIMUM_PAGES: u32 = 32;
static NEXT: AtomicU32 = AtomicU32::new(0);

struct BumpAllocator;

#[global_allocator]
static GLOBAL_ALLOCATOR: BumpAllocator = BumpAllocator;

extern "C" { static __heap_base: u8; }

#[inline(always)]
fn trap() -> ! { core::arch::wasm32::unreachable() }

#[inline(always)]
fn align_to(value: u32, alignment: u32) -> u32 {
    if alignment < 8 || !alignment.is_power_of_two() { trap(); }
    value.checked_add(alignment - 1)
        .map(|aligned| aligned & !(alignment - 1))
        .unwrap_or_else(|| trap())
}

#[inline(always)]
fn heap_base() -> u32 {
    align_to(core::ptr::addr_of!(__heap_base) as u32, 8)
}

#[inline(always)]
fn ensure_memory(required: u32) {
    let pages = core::arch::wasm32::memory_size::<0>() as u32;
    if pages > MAXIMUM_PAGES { trap(); }
    let current = pages.checked_mul(65_536).unwrap_or_else(|| trap());
    if required <= current { return; }
    let missing = required.checked_sub(current).unwrap_or_else(|| trap());
    let grow = missing.checked_add(65_535).map(|value| value / 65_536).unwrap_or_else(|| trap());
    let target = pages.checked_add(grow).unwrap_or_else(|| trap());
    if target > MAXIMUM_PAGES { trap(); }
    if core::arch::wasm32::memory_grow::<0>(grow as usize) == usize::MAX { trap(); }
}

fn allocate(size: u32, alignment: u32) -> u32 {
    loop {
        let prior = NEXT.load(Ordering::Relaxed);
        let start = align_to(prior.max(heap_base()), alignment.max(8));
        let end = start.checked_add(size).unwrap_or_else(|| trap());
        let required = if size == 0 { start.checked_add(1).unwrap_or_else(|| trap()) } else { end };
        ensure_memory(required);
        if NEXT.compare_exchange_weak(prior, end, Ordering::Relaxed, Ordering::Relaxed).is_ok() {
            return start;
        }
    }
}

unsafe impl GlobalAlloc for BumpAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let size = u32::try_from(layout.size()).unwrap_or_else(|_| trap());
        let alignment = u32::try_from(layout.align()).unwrap_or_else(|_| trap());
        allocate(size, alignment) as *mut u8
    }

    unsafe fn dealloc(&self, _pointer: *mut u8, _layout: Layout) {}
}

#[no_mangle]
pub extern "C" fn holo_alloc(size: i32) -> i32 {
    if size < 0 { trap(); }
    let size = size as u32;
    if size > INPUT_CAP { trap(); }
    let start = allocate(size, 8);
    i32::try_from(start).unwrap_or_else(|_| trap())
}

#[no_mangle]
pub extern "C" fn holo_run(input_ptr: i32, input_len: i32) -> i64 {
    if input_ptr < 0 || input_len < 0 { trap(); }
    let input_ptr = input_ptr as u32;
    let input_len = input_len as u32;
    if input_len > INPUT_CAP { trap(); }
    let input_end = input_ptr.checked_add(input_len).unwrap_or_else(|| trap());
    let memory_bytes = (core::arch::wasm32::memory_size::<0>() as u32)
        .checked_mul(65_536).unwrap_or_else(|| trap());
    if input_end > memory_bytes { trap(); }

    let input = unsafe { core::slice::from_raw_parts(input_ptr as *const u8, input_len as usize) };
    let generated_output = crate::dispatch(input.to_vec());
    if generated_output.len() > OUTPUT_CAP as usize { trap(); }
    let output_len = generated_output.len();
    let output_ptr = allocate(u32::try_from(output_len).unwrap_or_else(|_| trap()), 8);
    let output_end = output_ptr.checked_add(u32::try_from(output_len).unwrap_or_else(|_| trap())).unwrap_or_else(|| trap());
    if input_ptr < output_end && output_ptr < input_end { trap(); }
    unsafe { core::ptr::copy_nonoverlapping(generated_output.as_ptr(), output_ptr as *mut u8, output_len); }
    let packed = (u64::from(output_ptr) << 32) | u64::try_from(output_len).unwrap_or_else(|_| trap());
    packed as i64
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo<'_>) -> ! { trap() }
}
