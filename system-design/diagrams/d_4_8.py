"""Diagrams for note 4.8 - Computer architecture and the memory hierarchy."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def von_neumann():
    render("4-8-von-neumann", f"""
    rankdir=LR;
    cpu [label="CPU\\lcontrol unit + ALU", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    bus [label="ONE shared bus\\l(the von Neumann\\lbottleneck)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    mem [label="ONE memory\\l(instructions AND data,\\lindistinguishable -\\lboth just binary-encoded\\lbits at some address)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    cpu -> bus [dir=both, label="  fetch instruction\\l  OR read/write data\\l  (never both at once)"];
    bus -> mem [dir=both];

    note [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
         label="Four principles: (1) memory and processing unit are SEPARATE\\l(2) both instructions and data live in that one addressable\\lmemory (3) control flows via explicit commands (a program\\lcounter driving fetch-decode-execute) (4) everything - code\\land data alike - is BINARY ENCODED, no type distinction the\\lhardware enforces. Nearly every general-purpose CPU today.\\l"];
    mem -> note [style=invis];
    """)


def harvard():
    render("4-8-harvard", f"""
    rankdir=LR;
    cpu [label="CPU", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    ibus [label="instruction bus", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    dbus [label="data bus", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    imem [label="Instruction memory\\l(separate)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    dmem [label="Data memory\\l(separate)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];

    cpu -> ibus -> imem [dir=both];
    cpu -> dbus -> dmem [dir=both];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Can fetch the NEXT instruction and read/write data in the SAME\\lcycle - no shared-bus bottleneck. Costs two separate memories\\land buses, and code can't be treated as data (no self-modifying\\lcode, no easy JIT). Common in microcontrollers/DSPs; modern\\lgeneral CPUs are von Neumann overall but go 'Harvard-ish' at\\lthe L1 cache level specifically - separate L1 instruction and\\ldata caches (4.9), for exactly this same-cycle-access reason.\\l"];
    dmem -> note [style=invis];
    """)


def memory_hierarchy():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 6))
    levels = [
        ("Registers", "~1 KB", "~1 cycle (<1 ns)", 6, LIGHTBLUE, BLUE),
        ("L1 cache", "~32-64 KB", "~1 ns", 5, LIGHTBLUE, BLUE),
        ("L2 cache", "~256 KB-1 MB", "~4 ns", 4, LIGHTTEAL, TEAL),
        ("L3 cache", "~8-32 MB", "~15-20 ns", 3, LIGHTTEAL, TEAL),
        ("RAM (DRAM)", "GBs", "~100 ns", 2, LIGHTAMBER, AMBER),
        ("SSD / HDD", "TBs", "~16 us - 2 ms", 1, GRAY, SLATE),
    ]
    max_w = 10
    widths = [max_w - i*1.4 for i in range(len(levels))]
    for (name, size, latency, y, face, edge), w in zip(levels, widths):
        ax.barh(y, w, height=0.8, color=face, edgecolor=edge, align="center")
        ax.text(0, y, f"  {name}", ha="left", va="center", fontsize=10, fontweight="bold")
        ax.text(w + 0.2, y, f"{size}   |   {latency}", ha="left", va="center", fontsize=9, color=SLATE)
    ax.set_xlim(0, max_w + 7)
    ax.set_ylim(0.3, 6.8)
    ax.axis("off")
    ax.set_title("The memory hierarchy: smaller/faster (top) to larger/slower (bottom)",
                 loc="left", pad=12)
    return save_mpl(fig, "4-8-memory-hierarchy")


def sram_vs_dram():
    plt = mpl()
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.axis("off")
    rows = [
        ("", "SRAM", "DRAM"),
        ("used for", "registers, CPU caches", "main memory (RAM)"),
        ("cell", "6 transistors, no capacitor", "1 transistor + 1 capacitor"),
        ("needs refresh?", "no", "yes (capacitor leaks - re-read/\nrewrite thousands of times/sec)"),
        ("speed", "faster", "slower"),
        ("density / cost per bit", "lower density, pricier", "higher density, cheaper"),
    ]
    for i, row in enumerate(rows):
        y = len(rows) - i
        weight = "bold" if i == 0 else "normal"
        ax.text(0.02, y, row[0], fontsize=9.5, fontweight=weight, color=SLATE)
        ax.text(0.34, y, row[1], fontsize=9.5, fontweight=weight, color=BLUE)
        ax.text(0.67, y, row[2], fontsize=9.5, fontweight=weight, color=TEAL)
        if i == 0:
            ax.axhline(y - 0.35, xmin=0.02, xmax=0.98, color=INK, lw=1.2)
        else:
            ax.axhline(y - 0.35, xmin=0.02, xmax=0.98, color=GRAY, lw=0.6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(rows) + 0.6)
    ax.set_title("SRAM vs DRAM: the speed/density trade that shapes the whole hierarchy",
                 loc="left", pad=10)
    return save_mpl(fig, "4-8-sram-vs-dram")


def registers():
    render("4-8-registers", f"""
    rankdir=TB;
    root [label="CPU registers", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    gp [label="General purpose\\l(EAX, EBX, ECX, EDX...)\\lhold values for arithmetic,\\lfunction args, temporaries", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    sp [label="Special purpose", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    esp [label="ESP - stack pointer\\l(top of the current stack frame)", fillcolor="white"];
    ebp [label="EBP - base pointer\\l(bottom of the current frame,\\lfixed reference for locals/args)", fillcolor="white"];
    pc [label="Program counter / instruction\\lpointer - EIP/RIP", fillcolor="white"];
    flags [label="Flags register\\l(zero, carry, overflow...)", fillcolor="white"];
    nonuser [label="Non-user-accessible\\l(control/status registers -\\lonly the OS/kernel touches\\lthese directly)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    avx [label="Vector extensions (AVX)\\lwide registers (256/512-bit)\\lholding several values at once\\l- one instruction operates on\\lall of them in parallel (SIMD)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    root -> gp; root -> sp; root -> nonuser; root -> avx;
    sp -> esp; sp -> ebp; sp -> pc; sp -> flags;
    """)


if __name__ == "__main__":
    von_neumann()
    harvard()
    memory_hierarchy()
    sram_vs_dram()
    registers()
