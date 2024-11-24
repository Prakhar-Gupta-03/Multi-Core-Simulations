# Multi-Core Simulations with Cache Coherence Protocols

## Overview

This project investigates the impact of cache coherence protocols on the performance and scalability of multi-core systems within chiplet-based architectures. Using the gem5 simulator and the PARSEC benchmark suite, we focus on simulating systems with the MESI (Modified, Exclusive, Shared, Invalid) protocol for intra-chiplet cache coherence. Additionally, we explore the Garnet standalone protocol for inter-chiplet communication.

## Methodology

### Simulations and Benchmarks

1.	Single-Chiplet Multi-Core Systems:
- Simulated using the MESI 2-level cache coherence protocol.
- Benchmarks: bodytrack and ferret from the PARSEC suite.
- Core counts varied (2, 4, 8, and 16) to study L2 cache performance (miss/hit rates).
- Evaluated the impact of core count on system performance.
2.	Mesh Architecture:
- Attempted implementation of multi-chiplet systems with the Garnet standalone protocol.
- Challenges in integrating MESI with Garnet prevented full execution.
- Focused on testing the interconnection network using synthetic traffic patterns.
  4.	Multi-Chiplet Multi-Core Systems:
- Planned architecture with 16 cores organized into 4 chiplets.
- Each chiplet: 4 cores, private L1/L2 caches, and shared L3 cache.
- Intra-chiplet coherence via MESI; inter-chiplet coherence intended with Garnet.

### Methods and Setup

#### Building PARSEC Disk Image

The PARSEC benchmark suite evaluates multi-core performance with diverse workloads. The disk image for PARSEC benchmarks was prepared for use with gem5.
	1.	Setup:
- Clone and organize the PARSEC repository:
```bash
git clone https://github.com/darchr/parsec-benchmark
```

- Build the m5 utility and disk image:
```bash
git clone https://github.com/gem5/gem5
cd gem5/util/m5
scons build/x86/out/m5
cd disk-image
./build.sh
```

2.	Run Example Scripts:
- Use PARSEC benchmarks with gem5:
```bash
build/X86/gem5.opt \
configs/example/gem5_library/x86-parsec-benchmarks.py \
--benchmark <benchmark_program> --size <size>
```

- Parameters:
  - --benchmark: Choose from 13 programs (e.g., bodytrack, ferret).
  - --size: Workload size (test, simsmall, simmedium, simlarge).

#### Multi-Core Single-Chiplet Systems

	1.	Build gem5 with MESI:

scons build/X86/gem5.opt RUBY_PROTOCOL_MESI_TWO_LEVEL=y


	2.	Run Simulation:

build/X86/gem5.opt \
configs/example/gem5_library/x86-parsec-mesi2.py

#### Multi-Core Mesh Architecture

1.	Build Garnet Standalone:
```bash
scons build/X86/gem5.debug RUBY_PROTOCOL_GARNET_STANDALONE=y
```

2.	Run Synthetic Traffic Simulation:
```bash
./build/X86/gem5.debug \
configs/example/garnet_synth_traffic.py \
--num-cpus=16 --network=garnet --topology=Mesh_XY \
--mesh-rows=4 --sim-cycles=1000 --synthetic=uniform_random
```
## Experimental Observations

- Benchmarks Used: bodytrack and ferret.
- Configurations: Simulated 2, 4, 8, and 16 cores using MESI 2-level protocol.
- Key Metrics:
  - L2 cache miss and hit rates.
  - Scalability with increased core counts.
  - Simulations were limited to 3-minute runs due to time constraints.

## Future Work

- Develop a custom cache coherence protocol for multi-chiplet architectures.
- Extend simulations for complete runtime and analyze additional PARSEC benchmarks.
- Optimize inter-chiplet communication using Garnet in conjunction with MESI.