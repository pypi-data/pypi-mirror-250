from dwat import load_dwarf, NamedTypes

vmlinux = open("/home/jmill/kernel-junk/kernel-dbg/vmlinux", "rb")
dwarf = load_dwarf(vmlinux)

simple_xattr = dwarf.lookup_type(NamedTypes.Struct, "simple_xattr")
print(simple_xattr)

