import argparse
import time

import m5
from m5.objects import Root

from gem5.coherence_protocol import CoherenceProtocol
from gem5.components.boards.x86_board import X86Board
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires

# Check for the required gem5 build
requires(
    isa_required=ISA.X86,
    coherence_protocol_required=CoherenceProtocol.MESI_THREE_LEVEL,
)

# List of benchmark programs for parsec
benchmark_choices = [
    "blackscholes",
    "bodytrack",
    "canneal",
    "dedup",
    "facesim",
    "ferret",
    "fluidanimate",
    "freqmine",
    "raytrace",
    "streamcluster",
    "swaptions",
    "vips",
    "x264",
]

# Input size options
size_choices = ["test", "simsmall", "simmedium", "simlarge"]

parser = argparse.ArgumentParser(
    description="Configuration script to run the PARSEC benchmarks."
)
parser.add_argument(
    "--benchmark",
    type=str,
    required=True,
    help="Input the benchmark program to execute.",
    choices=benchmark_choices,
)
parser.add_argument(
    "--size",
    type=str,
    required=True,
    help="Simulation size of the benchmark program.",
    choices=size_choices,
)
args = parser.parse_args()

# Set up cache hierarchy: MESI Three Level Cache Hierarchy
from gem5.components.cachehierarchies.ruby.mesi_three_level_cache_hierarchy import (
    MESIThreeLevelCacheHierarchy,
)

cache_hierarchy = MESIThreeLevelCacheHierarchy(
    l1d_size="32KiB",
    l1d_assoc=4,
    l1i_size="32KiB",
    l1i_assoc=4,
    l2_size="256KiB",
    l2_assoc=4,
    l3_size="4MiB",
    l3_assoc=16,
    num_l3_banks=1,
)

# Memory: Dual Channel DDR4 2400 DRAM device
memory = DualChannelDDR4_2400(size="3GiB")

# Set up the processor with O3 CPU
processor = SimpleProcessor(
    cpu_type=CPUTypes.O3,
    isa=ISA.X86,
    num_cores=4,
)

# Configure the X86 board for full-system simulation
board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set up the workload: PARSEC benchmark
command = (
    f"cd /home/gem5/parsec-benchmark;"
    + "source env.sh;"
    + f"parsecmgmt -a run -p {args.benchmark} -c gcc-hooks -i {args.size} -n 2;"
    + "sleep 5;"
    + "m5 exit;"
)
board.set_kernel_disk_workload(
    kernel=obtain_resource("x86-linux-kernel-4.19.83", resource_version="1.0.0"),
    disk_image=obtain_resource("x86-parsec", resource_version="1.0.0"),
    readfile_contents=command,
)

# Handle different exit events during the simulation
def handle_workbegin():
    print("Done booting Linux")
    print("Resetting stats at the start of ROI!")
    m5.stats.reset()
    yield False

def handle_workend():
    print("Dump stats at the end of the ROI!")
    m5.stats.dump()
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: handle_workbegin(),
        ExitEvent.WORKEND: handle_workend(),
    },
)

# Start the simulation and track the wall clock time
globalStart = time.time()

print("Running the simulation with O3 CPU")
m5.stats.reset()

simulator.run()

print("All simulation events were successful.")
print("Done with the simulation")
print("Performance statistics:")
print("Simulated time in ROI: " + str(simulator.get_roi_ticks()[0]))
print("Ran a total of", simulator.get_current_tick() / 1e12, "simulated seconds")
print("Total wallclock time: %.2fs, %.2f min" % (time.time() - globalStart, (time.time() - globalStart) / 60))
