# import argparse
# import time
# import m5
# from m5.objects import Root
# from m5.objects import DDR4_2400_8x8
# from m5.util import addToPath
# from gem5.components.cachehierarchies.ruby.mesi_three_level_cache_hierarchy import MESIThreeLevelCacheHierarchy
# from gem5.components.processors.simple_processor import SimpleProcessor
# from gem5.components.boards.simple_board import SimpleBoard
# from gem5.components.memory.single_channel import SingleChannelDDR4_2400
# from gem5.isas import ISA
# from gem5.components.processors.cpu_types import CPUTypes
# from gem5.components.cachehierarchies.abstract_cache_hierarchy import AbstractCacheHierarchy
# from gem5.components.processors.abstract_processor import AbstractProcessor
# from gem5.components.memory.abstract_memory_system import AbstractMemorySystem
# from gem5.coherence_protocol import CoherenceProtocol

# # Adding the path to access the demo hello program
# addToPath('../../') 

# # Setting up the cache hierarchy
# cache_hierarchy = MESIThreeLevelCacheHierarchy(
#     l1i_size="32KiB",
#     l1i_assoc="4",
#     l1d_size="32KiB",
#     l1d_assoc="4",
#     l2_size="256KiB",
#     l2_assoc="4",
#     l3_size="4MiB",
#     l3_assoc="16",
#     num_l3_banks=1  # Shared L3 amongst cores
# )

# # Setting up a 4-core RISC-V CPU
# processor = SimpleProcessor(
#     cpu_type=CPUTypes.O3,  # Out of order CPU
#     isa=ISA.RISCV,
#     num_cores=4,  # 4-core setup
# )

# # Defining the memory system
# memory = SingleChannelDDR4_2400(size="4GiB")  # 4GiB DDR4 memory

# # Creating the board with processor, memory, and cache hierarchy
# board = SimpleBoard(
#     clk_freq="3GHz",  # Clock frequency of the system
#     processor=processor,
#     memory=memory,
#     cache_hierarchy=cache_hierarchy
# )

# # Setting the binary to run (hello program in this case)
# board.set_se_binary_workload("tests/test-progs/hello/bin/riscv/linux/hello")

# # Root of the simulation
# root = Root(full_system=False, system=board)

# # Running the simulation
# m5.instantiate()

# print("Starting simulation!")
# exit_event = m5.simulate()

# print(f"Exited @ tick {m5.curTick()} because {exit_event.getCause()}")



# import m5
# from m5.objects import *
# m5.util.addToPath("../../")
# import os
# from common.FileSystemConfig import config_filesystem
# from MESITwoLevelCache import MESITwoLevelCache

# # Setup the system
# system = System()

# # Create clock and voltage domains
# system.clk_domain = SrcClockDomain()
# system.clk_domain.clock = "1GHz"
# system.clk_domain.voltage_domain = VoltageDomain()

# system.mem_mode = "timing"  # Use timing accesses
# system.mem_ranges = [AddrRange("512MB")]

# system.cpu = [RiscvTimingSimpleCPU () for i in range(2)]

# system.mem_ctrl = MemCtrl()
# system.mem_ctrl.dram = DDR3_1600_8x8()
# system.mem_ctrl.dram.range = system.mem_ranges[0]

# for cpu in system.cpu:
#     cpu.createInterruptController()

# system.caches = MESITwoLevelCache()
# # system.caches.setup(system, system.cpu, [system.mem_ctrl])
# system.caches.setup(system, system.cpu, [system.mem_ctrl], [], system.mem_ctrl)

# # Create a process for running "hello" and set it as the workload for the CPU
# binary = '/path/to/gem5/tests/test-progs/hello/bin/riscv/linux/hello'
# process = Process()
# process.cmd = [binary]
# for cpu in system.cpu:
#     cpu.workload = process
#     cpu.createThreads()

# # Setup and run simulation
# root = Root(full_system=False, system=system)
# m5.instantiate()

# print("Running simulation with 4-core system using MESI_Two_Level protocol...")
# exit_event = m5.simulate()

# print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))
import m5

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_two_level_cache_hierarchy import (
    MESITwoLevelCacheHierarchy
)
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator

import os
from argparse import ArgumentParser

def main():
    suite_obj = obtain_resource("riscv-getting-started-benchmark-suite")
    workloads = list(suite_obj.with_input_group('se'))
    base_outdir = m5.options.outdir
    run_workload(setup_board(), workloads[0])

def setup_board():
    # Create cache hierarchy
    cache_hierarchy = MESITwoLevelCacheHierarchy(
        l1d_size="16kB",
        l1d_assoc=8,
        l1i_size="16kB",
        l1i_assoc=8,
        l2_size="256kB",
        l2_assoc=16,
        num_l2_banks=1,
    )

    # Create memory
    memory = SingleChannelDDR3_1600(size="8GB")

    # Create processor
    processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, isa=ISA.RISCV, num_cores=4)

    # Create board
    return SimpleBoard(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )

def run_workload(board, binary_path):
    print(f'--> Running workload "{binary_path}"')

    # Set the workload
    board.set_workload(binary_path)

    # Create and run the simulator
    simulator = Simulator(board=board)
    simulator.run()

if __name__ == '__m5_main__':
    main()
