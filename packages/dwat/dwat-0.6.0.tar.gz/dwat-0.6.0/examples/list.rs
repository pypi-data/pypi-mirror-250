/// Example of doing struct analysis to find those which
/// have members that are of list_head structs
use dwat::prelude::*;
use dwat::Dwarf;
use std::fs::File;
use memmap2::Mmap;

fn main() -> anyhow::Result<()> {
    let mut args = std::env::args().skip(1);
    let path = args.next().unwrap_or_else(|| {
        eprintln!("Usage: lists <path>");
        std::process::exit(1);
    });

    let file = File::open(path).unwrap();
    let mmap = unsafe { Mmap::map(&file) }?;
    let dwarf = Dwarf::load(&*mmap)?;

    let structs = dwarf.get_fg_named_structs_map()?;

    for (key, struc) in structs.into_iter() {
        for memb in struc.members(&dwarf)? {
            let mtype = memb.get_type(&dwarf)?;
            if let dwat::Type::Struct(inner_struct) = mtype {
                if let Ok(inner_name) = inner_struct.name(&dwarf) {
                    if inner_name == String::from("list_head") {
                        println!("struct {}", key.name);
                    }
                }
            }
        }
    };

    Ok(())
}
