## Setup

Steps to run and compile: 

1. Setup `gem5` using the tutorial present [here](https://www.gem5.org/documentation/learning_gem5/part1/building/). 

2. Run the following commands to set up gem5 with MESI Three Level Protocol: 

```bash
cd gem5
mkdir build_MESI
scons defconfig build_MESI/RISCV_MESI_3L build_opts/RISCV
scons setconfig build_MESI/RISCV_MESI_3L RUBY_PROTOCOL_MESI_THREE_LEVEL=y
scons build_MESI/RISCV_MESI_3L/gem5.opt -j 8
```

Run the following commands to set up gem5 with MESI Two Level Protocol: 

```bash
cd gem5
scons defconfig build_MESI/RISCV_MESI_2L build_opts/RISCV
scons setconfig build_MESI/RISCV_MESI_2L RUBY_PROTOCOL_MESI_TWO_LEVEL=y
scons build_MESI/RISCV_MESI_2L/gem5.opt -j 8
```

We create a new build directory instead of using `build` to avoid conflicts with the default `build` directory as per the [docs](https://www.gem5.org/documentation/general_docs/kconfig_build_system/). 


## Running simulation

To run the simulation with MESI Three Level Protocol, run the following commands after moving `mesi_three_level.py` to `configs/learning_gem5/Project/`: 

```bash
build_MESI/RISCV_MESI_3L/gem5.opt configs/learning_gem5/Project/mesi_three_level.py
```

The above command will run simulation with MESI Three Level Protocol for the benchmark chosen in the function `obtain_resource()` in `mesi_three_level.py`.

To run the simulation with MESI Two Level Protocol, run the following commands after moving `mesi_two_level.py` to `configs/learning_gem5/Project/`: 

```bash
build_MESI/RISCV_MESI_2L/gem5.opt configs/learning_gem5/Project/mesi_two_level.py
```

## Benchmarks tried to run 

1. `riscv-getting-started-benchmark-suite`: 

We tried to run the [RISCV getting started benchmark](https://resources.gem5.org/resources/riscv-getting-started-benchmark-suite/raw?database=gem5-resources&version=1.0.0) for different input_groups - `llvm`, `matrix-multiply` and `minisat`. 

Output log for the `matrix-multiply` simulation with MESI Three Level Protocol is - 

```
gem5 Simulator System.  https://www.gem5.org
gem5 is copyrighted software; use the --copyright option for details.

gem5 version 24.0.0.1
gem5 compiled Oct 24 2024 23:36:18
gem5 started Oct 25 2024 18:39:40
gem5 executing on prakhar, pid 113726
command line: build_MESI/RISCV_MESI_3L/gem5.opt configs/learning_gem5/Project/mesi_three_level.py

info: Using default config
--> Running workload "riscv-matrix-multiply-run"
Resource 'riscv-matrix-multiply' was not found locally. Downloading to '/root/.cache/gem5/riscv-matrix-multiply'...
Finished downloading resource 'riscv-matrix-multiply'.
Global frequency set at 1000000000000 ticks per second
warn: No dot file generated. Please install pydot to generate the dot file and pdf.
src/mem/dram_interface.cc:690: warn: DRAM device capacity (16384 Mbytes) does not match the address range assigned (4096 Mbytes)
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
board.remote_gdb: Listening for connections on port 7000
src/sim/simulate.cc:199: info: Entering event queue @ 0.  Starting simulation...
src/mem/ruby/system/Sequencer.cc:680: warn: Replacement policy updates recently became the responsibility of SLICC state machines. Make sure to setMRU() near callbacks in .sm files!
src/sim/syscall_emul.cc:85: warn: ignoring syscall set_robust_list(...)
      (further warnings will be suppressed)
src/sim/syscall_emul.hh:1075: warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
      Returning '/root/.cache/gem5/riscv-matrix-multiply'
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/syscall_emul.cc:74: warn: ignoring syscall mprotect(...)
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
Populating the first and second matrix...
Done!
Multiplying the matrixes...
Done!
Calculating the sum of all elements in the matrix...
Done
The sum is 57238500000
```

Simulation for `llvm` took very long to run, and hence we clipped it short, however the output log is as follows - 

```
gem5 version 24.0.0.1
gem5 compiled Oct 24 2024 23:36:18
gem5 started Oct 25 2024 18:46:35
gem5 executing on prakhar, pid 116817
command line: build_MESI/RISCV_MESI_3L/gem5.opt configs/learning_gem5/Project/mesi_three_level.py

info: Using default config
--> Running workload "riscv-llvm-minisat-run"
Resource 'riscv-llvm-minisat' was not found locally. Downloading to '/root/.cache/gem5/riscv-llvm-minisat'...
Finished downloading resource 'riscv-llvm-minisat'.
Resource 'llvm-minisat-cnf-input' was not found locally. Downloading to '/root/.cache/gem5/llvm-minisat-cnf-input'...
Finished downloading resource 'llvm-minisat-cnf-input'.
Global frequency set at 1000000000000 ticks per second
warn: No dot file generated. Please install pydot to generate the dot file and pdf.
src/mem/dram_interface.cc:690: warn: DRAM device capacity (16384 Mbytes) does not match the address range assigned (4096 Mbytes)
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
src/base/statistics.hh:279: warn: One of the stats is a legacy stat. Legacy stat is a stat that does not belong to any statistics::Group. Legacy stat is deprecated.
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
src/arch/riscv/isa.cc:276: info: RVV enabled, VLEN = 256 bits, ELEN = 64 bits
board.remote_gdb: Listening for connections on port 7000
src/sim/simulate.cc:199: info: Entering event queue @ 0.  Starting simulation...
src/mem/ruby/system/Sequencer.cc:680: warn: Replacement policy updates recently became the responsibility of SLICC state machines. Make sure to setMRU() near callbacks in .sm files!
src/sim/syscall_emul.hh:1075: warn: readlink() called on '/proc/self/exe' may yield unexpected results in various settings.
      Returning '/root/.cache/gem5/riscv-llvm-minisat'
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/syscall_emul.cc:74: warn: ignoring syscall mprotect(...)
This is MiniSat 2.0 beta
Reading from standard input... Use '-h' or '--help' for help.
============================[ Problem Statistics ]=============================
|                                                                             |
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
src/sim/mem_state.cc:448: info: Increasing stack size by one page.
|  Number of variables:  65902                                                |
|  Number of clauses:    218335                                               |
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000190000-0x4000000000231000, adding 221184
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000190000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000231000-0x4000000000267000, adding 73728
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000231000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x400000000029d000-0x400000000038e000, adding 327680
src/sim/syscall_emul.hh:1393: warn: returning 0x400000000029d000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x400000000038e000-0x40000000003df000, adding 110592
src/sim/syscall_emul.hh:1393: warn: returning 0x400000000038e000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x40000000003df000-0x4000000000430000, adding 110592
src/sim/syscall_emul.hh:1393: warn: returning 0x40000000003df000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000459000-0x40000000005c2000, adding 491520
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000459000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x40000000005c2000-0x400000000063b000, adding 163840
src/sim/syscall_emul.hh:1393: warn: returning 0x40000000005c2000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000678000-0x40000000006f1000, adding 163840
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000678000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x40000000006f1000-0x400000000072e000, adding 81920
src/sim/syscall_emul.hh:1393: warn: returning 0x40000000006f1000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x400000000076b000-0x4000000000988000, adding 737280
src/sim/syscall_emul.hh:1393: warn: returning 0x400000000076b000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000988000-0x4000000000a3d000, adding 245760
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000988000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000a3d000-0x4000000000a98000, adding 122880
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000a3d000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000a98000-0x4000000000b4d000, adding 245760
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000a98000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000b4d000-0x4000000000ba8000, adding 122880
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000b4d000 as start
src/sim/syscall_emul.hh:1374: warn: mremapping to new vaddr 0x4000000000ba8000-0x4000000000c03000, adding 122880
src/sim/syscall_emul.hh:1393: warn: returning 0x4000000000ba8000 as start
```

2. PARSEC Benchmark Suite:

We tried to run the PARSEC benchmark suite, however, ran into various issues with setting it up for MESI Three Level compiled gem5 build. Following along the tutorial [here](https://www.gem5.org/documentation/gem5art/tutorials/parsec-tutorial), we ran into issues setting up due to an inaccesible link. Trying to retrieve the same through WayBack Machine also failed. 

We are still trying to figure out how to setup and run the benchmark. 

## Code Structure

The code is structured into functions as follows: 
1. `main()`: Extracting parameters and setting up the benchmark suite, followed by calling the method for workload simulation. 
2. `setup_board()`: Invoking the MESI Three Level Cache Heirarchy along with CPU, Memory and Caches configurations. The memory, processor and board is set up here. 
3. `run_workload()`: Running of the simulation is performed here along with final dumping of results into the stats.txt file. 

## Issues in Replicating System

1. Directory Memory System: DDR4_2400 model that is present in the paper requires a 4x4 processor's memory system with 4 GiB space and 1 KiB row buffer, however, none of the source code's provided DDR models have the same. 

2. Cache Setup: The cache line size of 64 bytes is not set up explicitly, and it is rather determined by the cache heirarchy methods when invoked using `CacheHeirarchyMESIThreeLevel()`. 

