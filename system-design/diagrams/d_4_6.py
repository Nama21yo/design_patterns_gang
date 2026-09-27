"""Diagrams for note 4.6 - Virtual memory, paging, and the MMU."""
from _style import (render, mpl, save_mpl, INK, SLATE, BLUE, TEAL, AMBER, RED,
                    GRAY, LIGHTBLUE, LIGHTTEAL, LIGHTAMBER)


def why_virtual_memory():
    render("4-6-why-virtual-memory", f"""
    rankdir=LR;

    subgraph cluster_bad {{
        label="Without virtual memory: processes share raw physical addresses";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        p1 [label="Process A\\l'my array is at\\laddress 0x4000'", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        p2 [label="Process B\\l'my array is ALSO\\lat address 0x4000'", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
        mem [label="Physical RAM\\l0x4000 can only be\\lONE thing", fillcolor="{RED}", fontcolor=white, color="{RED}"];
        p1 -> mem; p2 -> mem;
        note1 [shape=note, fillcolor="{RED}", fontcolor=white, color="{RED}",
              label="collision, no isolation, one process can read/corrupt\\lanother's memory, and every program must be linked\\lagainst wherever it happens to load in RAM\\l"];
        mem -> note1 [style=invis];
    }}

    subgraph cluster_good {{
        label="With virtual memory: every process gets its own full address space";
        fontname="DejaVu Sans"; fontsize=11; color="{SLATE}"; style=dashed;
        va [label="Process A's virtual\\laddress 0x4000", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        vb [label="Process B's virtual\\laddress 0x4000", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
        mmu [label="MMU: translates\\leach process's 0x4000\\lto a DIFFERENT real\\lphysical frame", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
        pa [label="physical frame 1", fillcolor="{GRAY}"];
        pb [label="physical frame 2", fillcolor="{GRAY}"];
        va -> mmu; vb -> mmu; mmu -> pa; mmu -> pb;
        note2 [shape=note, fillcolor="{LIGHTTEAL}", color="{TEAL}",
              label="isolation (A cannot even address B's memory), every\\lprocess can be linked as if it owns address 0 upward,\\land a process can be given the ILLUSION of more memory\\lthan physically exists (pages swapped to disk on demand)\\l"];
        mmu -> note2 [style=invis];
    }}
    """)


def address_translation_tlb():
    render("4-6-address-translation-tlb", f"""
    rankdir=LR;
    cpu [label="CPU\\l(compiler emits\\lLoad/Store on\\lVIRTUAL addresses)", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    tlb [label="TLB check\\l(small, fast cache of\\lrecent translations)", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    hit [label="TLB HIT\\l-> physical address\\limmediately (~1 cycle)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    miss [label="TLB MISS\\l-> walk the page table\\lin memory (slow),\\lcache the result in\\lthe TLB for next time", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    check [label="MMU: legal address?\\l(within this process's\\lmapped pages?)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    ram [label="RAM\\l(physical address)", fillcolor="{GRAY}", color="{SLATE}"];
    exc [label="Illegal Access\\lException -> signal\\lto the CPU/process\\l(segfault)", fillcolor="{RED}", fontcolor=white, color="{RED}"];

    cpu -> tlb;
    tlb -> hit [label="  (~99% of the time)"];
    tlb -> miss [label="  (rare)"];
    miss -> check;
    hit -> ram;
    check -> ram [label="  legal"];
    check -> exc [label="  illegal"];
    exc -> cpu [style=dashed, color="{SLATE}"];
    """)


def paging():
    render("4-6-paging", f"""
    rankdir=LR;
    va [label="Virtual address\\lpage number | offset", fillcolor="{INK}", fontcolor=white, color="{INK}"];
    pt [label="Page table\\l(one entry per virtual page:\\lpage number -> frame number,\\l+ present/valid, permissions)", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    frame [label="Physical frame\\l(same size as a page,\\le.g. 4 KB)", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    disk [label="Not present ->\\lPAGE FAULT: OS pauses\\lthe process, loads the\\lpage from disk/swap,\\lupdates the page table,\\lretries the instruction", fillcolor="{LIGHTAMBER}", color="{AMBER}"];

    va -> pt;
    pt -> frame [label="  present"];
    pt -> disk [label="  not present"];
    disk -> frame [label="  now loaded", style=dashed, color="{SLATE}"];

    note [shape=note, fillcolor="{GRAY}", color="{SLATE}",
         label="Pages are fixed-size, so the OS never has to find a\\l'big enough contiguous hole' in physical memory the\\lway a pre-paging allocator did - any free frame,\\lanywhere, works for any page. This is also exactly\\lwhat makes a page a natural unit to run an eviction\\lalgorithm (4.1) over when physical memory is full.\\l"];
    frame -> note [style=invis];
    """)


def memory_layout():
    render("4-6-memory-layout", f"""
    rankdir=TB;
    node [shape=box, width=2.6];
    high [label="High addresses", shape=plaintext, fillcolor=none, color=none];
    stack [label="Stack\\lfunction calls, local vars\\lGROWS DOWNWARD", fillcolor="{LIGHTBLUE}", color="{BLUE}"];
    gap [label="(unused gap)", shape=plaintext, fillcolor=none, color=none, fontcolor="{SLATE}"];
    heap [label="Heap\\lmalloc / new - dynamic,\\lprogrammer/runtime managed\\lGROWS UPWARD", fillcolor="{LIGHTTEAL}", color="{TEAL}"];
    bss [label="BSS + Data segment\\lglobal / static variables", fillcolor="{LIGHTAMBER}", color="{AMBER}"];
    text [label="Text / Code segment\\lthe compiled instructions\\l(read-only)", fillcolor="{GRAY}", color="{SLATE}"];
    low [label="Low addresses", shape=plaintext, fillcolor=none, color=none];

    high -> stack -> gap -> heap -> bss -> text -> low [style=invis];
    stack -> gap [label="  can collide if\\l  either grows too far\\l  (stack overflow /\\l  heap exhaustion)", color="{RED}", fontcolor="{RED}", constraint=false];
    """)


if __name__ == "__main__":
    why_virtual_memory()
    address_translation_tlb()
    paging()
    memory_layout()
