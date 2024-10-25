import argparse
import time
import m5
from m5.objects import Root
from m5.objects import DDR4_2400_8x8
from m5.util import addToPath
from gem5.components.cachehierarchies.ruby.mesi_three_level_cache_hierarchy import MESIThreeLevelCacheHierarchy
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.isas import ISA
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.cachehierarchies.abstract_cache_hierarchy import AbstractCacheHierarchy
from gem5.components.processors.abstract_processor import AbstractProcessor
from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
from gem5.coherence_protocol import CoherenceProtocol

# Adding the path to access the demo hello program
addToPath('../../') 

# Setting up the cache hierarchy
cache_hierarchy = MESIThreeLevelCacheHierarchy(
    l1i_size="32KiB",
    l1i_assoc="4",
    l1d_size="32KiB",
    l1d_assoc="4",
    l2_size="256KiB",
    l2_assoc="4",
    l3_size="4MiB",
    l3_assoc="16",
    num_l3_banks=1  # Shared L3 amongst cores
)

# Setting up a 4-core RISC-V CPU
processor = SimpleProcessor(
    cpu_type=CPUTypes.O3,  # Out of order CPU
    isa=ISA.RISCV,
    num_cores=4,  # 4-core setup
)

# Defining the memory system
memory = SingleChannelDDR4_2400(size="4GiB")  # 4GiB DDR4 memory

# Creating the board with processor, memory, and cache hierarchy
board = SimpleBoard(
    clk_freq="3GHz",  # Clock frequency of the system
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

# Setting the binary to run (hello program in this case)
board.set_se_binary_workload("tests/test-progs/hello/bin/riscv/linux/hello")

# Root of the simulation
root = Root(full_system=False, system=board)

# Running the simulation
m5.instantiate()

print("Starting simulation!")
exit_event = m5.simulate()

print(f"Exited @ tick {m5.curTick()} because {exit_event.getCause()}")

