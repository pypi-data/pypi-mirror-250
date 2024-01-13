use std::fs::File;
use memmap2::Mmap;

use dwat::prelude::*;
use dwat::Dwarf;

fn main() -> anyhow::Result<()> {
    let mut args = std::env::args().skip(1);
    let path = args.next().unwrap_or_else(|| {
        eprintln!("Usage: range <path>");
        std::process::exit(1);
    });

    let file = File::open(path)?;
    let mmap = unsafe { Mmap::map(&file) }?;

    let dwarf = Dwarf::load(&*mmap)?;
    let struct_map = dwarf.get_fg_named_structs_map()?;

    for (key, dwstruct) in struct_map.into_iter() {
        if 64 < key.byte_size && key.byte_size <= 96 {
            println!("{}", dwstruct.to_string_verbose(&dwarf, 1)?);
        }
    };

    Ok(())
}
