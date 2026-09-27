"""Diagrams for note 4.10 - Storage media: RAM generations, SSD, HDD and RAID."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def ram_generations():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    gens = ["SDR\n(1x)", "DDR\n(2x)", "DDR4\n(2x, higher clock)", "QDR\n(4x, networking)"]
    transfers = [1, 2, 2, 4]
    colors = [GRAY, BLUE, TEAL, AMBER]
    ax.bar(gens, transfers, color=colors, width=0.5)
    for i, v in enumerate(transfers):
        ax.text(i, v + 0.08, f"{v}x per clock", ha="center", fontsize=9)
    ax.set_ylabel("data transfers per clock cycle")
    ax.set_title("SDR -> DDR -> QDR: same clock, more transfers per tick",
                 loc="left", pad=10)
    ax.set_ylim(0, 5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return save_mpl(fig, "4-10-ram-generations")


def ssd_structure():
    render("4-10-ssd-structure", f"""
    rankdir=TB;
    cell [label="One floating-gate transistor\\l= one cell", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    gate [label="Electrons trapped on an\\lISOLATED floating gate\\l-> charge stays put with\\lNO power applied\\l(this is what makes it 'flash')", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    bit [label="Charge level read as a bit\\l(SLC: 1 bit/cell, MLC: 2,\\lTLC: 3, QLC: 4 - more bits/cell\\l= cheaper, less durable, slower)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    page [label="Cells grouped into PAGES\\l(~4-16 KB) - read/write unit", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    block [label="Pages grouped into BLOCKS\\l(~MBs) - ERASE unit\\l(must erase a whole block\\lbefore rewriting any page in it)", fillcolor="{GRAY}", color="{SLATE}"];

    cell -> gate -> bit -> page -> block;
    """)


def nand_vs_nor():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8.5, 3))
    ax.axis("off")
    rows = [
        ("", "NAND", "NOR"),
        ("cell wiring", "series (like a NAND gate)", "parallel (like a NOR gate)"),
        ("density", "higher - smaller cells", "lower - larger cells"),
        ("access", "block/page (sequential-ish)", "byte-addressable random access"),
        ("used for", "SSDs, USB drives, bulk storage", "embedded firmware / boot code (XIP)"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.02, y, row[0], fontsize=9.5, fontweight=weight, color=SLATE)
        ax.text(0.30, y, row[1], fontsize=9.5, fontweight=weight, color=BLUE)
        ax.text(0.66, y, row[2], fontsize=9.5, fontweight=weight, color=TEAL)
        ax.axhline(y - 0.35, xmin=0.02, xmax=0.98, color=(INK if i == 0 else GRAY), lw=(1.2 if i==0 else 0.6))
    ax.set_xlim(0, 1); ax.set_ylim(0, len(rows) + 0.6)
    ax.set_title("NAND vs NOR flash", loc="left", pad=10)
    return save_mpl(fig, "4-10-nand-vs-nor")


def raid_levels():
    render("4-10-raid-levels", f"""
    rankdir=LR;
    r0 [label="RAID 0 - striping\\lspread data across N disks,\\lNO redundancy\\l-> fastest, 0 disks can fail", fillcolor="{RED}", fontcolor=white, color="{RED}"];
    r1 [label="RAID 1 - mirroring\\lfull duplicate copy\\l-> 50% usable capacity,\\lsurvives 1 disk lost per mirror", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    r5 [label="RAID 5 - striping + 1 parity\\lN disks: N-1 disks of usable\\lcapacity, survives ANY 1 disk lost", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    r6 [label="RAID 6 - striping + 2 parity\\lN-2 usable, survives ANY\\l2 disks lost simultaneously", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    r10 [label="RAID 10 - mirror THEN stripe\\lfast (like RAID 0) AND\\lredundant (like RAID 1),\\l50% usable capacity", fillcolor="{GRAY}", color="{SLATE}"];

    {{ rank=same; r0; r1; r5; r6; r10 }}
    """)


if __name__ == "__main__":
    ram_generations()
    ssd_structure()
    nand_vs_nor()
    raid_levels()
