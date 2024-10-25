import m5
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.ruby.mesi_three_level_cache_hierarchy import (
    MESIThreeLevelCacheHierarchy
)
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.simulate.exit_event import ExitEvent

import os
from argparse import ArgumentParser

def main():
    # Get workloads list -- getting started suite SE workloads
    suite_obj = obtain_resource("riscv-getting-started-benchmark-suite")
    workloads = list(suite_obj.with_input_group('minisat'))

    # Get workload index from arguments
    parser = ArgumentParser()
    parser.add_argument('workload_index', type=int, nargs='?', default=0, help="Index of the workload to run.")
    args = parser.parse_args()

    # Signal end of suite to caller
    if args.workload_index >= len(workloads):
        print('--> Invalid workload index. Suite completed or index out of range.')
        exit(1)

    # Remember base output directory
    base_outdir = m5.options.outdir

    # Setup board and run workload
    run_workload(setup_board(), workloads[args.workload_index], base_outdir)


def setup_board():
    # Create MESI Three-Level Cache Hierarchy with private L1 and L2, shared L3
    cache_hierarchy = MESIThreeLevelCacheHierarchy(
        l1i_size="32KiB",
        l1i_assoc="4",
        l1d_size="32KiB",
        l1d_assoc="4",
        l2_size="256KiB",
        l2_assoc="4",
        l3_size="4MB",
        l3_assoc="16",
        num_l3_banks=4
    )

    # Create memory
    memory = SingleChannelDDR4_2400(size="4GB")

    # Create processor (4-core RISCV O3)
    processor = SimpleProcessor(cpu_type=CPUTypes.O3, isa=ISA.RISCV, num_cores=4)

    # Create board
    return SimpleBoard(
        clk_freq="3GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )


def run_workload(board, workload, base_outdir):
    print(f'--> Running workload "{workload.get_id()}"')

    # Create output subdirectory for this specific benchmark
    m5.options.outdir = os.path.join(base_outdir, workload.get_id())
    try:
        os.mkdir(m5.options.outdir)
    except Exception:
        pass

    # Run workload
    board.set_workload(workload)
    simulator = Simulator(board=board)
    exit_event = simulator.run()

    # Check exit status of the simulation
    if exit_event.getCause() == ExitEvent.EXIT_SYSCALL:
        print("--> Workload completed successfully")
    else:
        print(f"--> Workload failed with exit event: {exit_event.getCause()}")

    # Reset m5 stats
    m5.stats.dump()
    m5.stats.reset()

    # Move stats file to the subdirectory
    in_stats = os.path.join(base_outdir, 'stats.txt')
    out_stats = os.path.join(m5.options.outdir, 'stats.txt')
    print(f'--> Workload complete, moving stats to {out_stats}')
    os.rename(in_stats, out_stats)


if __name__ == '__m5_main__':
    main()
