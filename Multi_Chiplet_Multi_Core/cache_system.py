import math

from m5.defines import buildEnv
from m5.objects import *
from m5.util import (
    fatal,
    panic,
)


class MyCacheSystem(RubySystem):
    def __init__(self):
        if buildEnv["PROTOCOL"] != "MSI":
            fatal("This system assumes MSI from learning gem5!")

        super().__init__()

    def setup(self, system, cpus, mem_ctrls):
        
        # Ruby's global network.
        self.intra_network = IntraChiplet(self)
        self.inter_network = InterChiplet(self)

        self.number_of_virtual_networks = 3
        self.intra_network.number_of_virtual_networks = 3
        self.inter_network.number_of_virtual_networks = 3

        self.dir_controller = [
            DirController(self, system.mem_ranges, mem_ctrls)
        ]
        self.intra_controllers = [L1Cache(system, self, cpu, math.floor(i/4)) for i, cpu in enumerate(cpus)] + [
            L2Cache(system, self, cpu, math.floor(i/4)) for i, cpu in enumerate(cpus)
        ] + self.dir_controller
        self.inter_controllers =  [
            L3Cache(system, self, cpu, math.floor(i)) for i, cpu in enumerate(cpus/4)
        ] + self.dir_controller

        # Create one sequencer per CPU. In many systems this is more
        # complicated since you have to create sequencers for DMA controllers
        # and other controllers, too.
        self.sequencers = [
            RubySequencer(
                version=i,
                # I/D cache is combined and grab from ctrl
                dcache=self.controllers[i].cacheMemory,
                clk_domain=self.controllers[i].clk_domain,
            )
            for i in range(len(cpus))
        ]

        # We know that we put the controllers in an order such that the first
        # N of them are the L1 caches which need a sequencer pointer
        for i, c in enumerate(self.intra_controllers[0 : len(self.sequencers)]):
            c.sequencer = self.sequencers[i]

        self.num_of_sequencers = len(self.sequencers)

        # Create the network and connect the controllers.
        # NOTE: This is quite different if using Garnet!
        self.intra_network.connectControllers(self.intra_controllers)
        self.intra_network.setup_buffers()

        self.inter_network.connectControllers(self.inter_controllers)
        self.inter_network.setup_buffers()
        # Set up a proxy port for the system_port. Used for load binaries and
        # other functional-only things.
        self.sys_port_proxy = RubyPortProxy()
        system.system_port = self.sys_port_proxy.in_ports

        # Connect the cpu's cache, interrupt, and TLB ports to Ruby
        for i, cpu in enumerate(cpus):
            self.sequencers[i].connectCpuPorts(cpu)


class L1Cache(L0Cache_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1
        return cls._version - 1

    def __init__(self, system, ruby_system, cpu, cluster_id):
        super().__init__()

        self.Icache = RubyCache(
            size="32kB",
            assoc=4,
            is_icache=True,
            start_index_bit=self.getBlockSizeBits(system),
            replacement_policy=LRURP()
        )
        self.Dcache = RubyCache(
            size="32kB",
            assoc=8,
            is_icache=False,
            start_index_bit=self.getBlockSizeBits(system),
            replacement_policy=LRURP()
        )

        self.cluster_id = cluster_id
        self.clk_domain = cpu.clk_domain
        self.send_evictions = True
        
        self.ruby_system = ruby_system
        self.version = self.versionCount()
        self.connectQueues(ruby_system)

    def getBlockSizeBits(self, cache_line_size):
        bits = int(math.log(cache_line_size, 2))
        if 2**bits != int(cache_line_size):
            raise Exception("Cache line size is not a power of 2!")
        return bits

    def connectQueues(self, network):
        self.prefetchQueue = MessageBuffer()
        self.mandatoryQueue = MessageBuffer()
        self.optionalQueue = MessageBuffer()

        
        self.bufferToL1 = MessageBuffer(ordered=True)
        self.bufferFromL1 = MessageBuffer(ordered=True)

class L2Cache(L1Cache_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1
        return cls._version - 1

    def __init__(self, system, ruby_system, cpu, cluster_id):
        super().__init__()

        # This is the cache memory object that stores the cache data and tags
        self.cache = RubyCache(
            size="256kB",
            assoc=4,
            start_index_bit=self.getBlockSizeBits(system),
            is_icache=False,
        )
        
        self.l2_select_num_bits = int(math.log(4, 2))
        self.cluster_id = cluster_id
        self.clk_domain = cpu.clk_domain
        self.prefetcher = RubyPrefetcher()
        self.transitions_per_cycle = 32
        
        self.l1_request_latency = 2
        self.l1_response_latency = 2
        self.to_l2_latency = 1

        self.version = self.versionCount()
        self.connectQueues(ruby_system)

class L3Cache(L2Cache_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1
        return cls._version - 1

    def __init__(self, system, ruby_system, cpu, cluster_id):
        super().__init__()


        self.L2cache = RubyCache(
            size="4MB",
            assoc=16,
            start_index_bit=self.getIndexBit(4, system),
        )

        self.transitions_per_cycle = 4
        self.cluster_id = cluster_id
        self.l2_request_latency = 2
        self.l2_response_latency = 2
        self.to_l1_latency = 1

        self.version = self.versionCount()
        self.connectQueues(ruby_system)

    def getIndexBit(self, num_l3Caches, cache_line_size):
        l3_bits = int(math.log(num_l3Caches, 2))
        bits = int(math.log(cache_line_size, 2)) + l3_bits
        return bits

    def connectQueues(self, network):
        # In the below terms, L1 and L2 are ruby backend terminology.
        # In stdlib, they are L2 and L3 caches respectively.
        self.DirRequestFromL2Cache = MessageBuffer()
        self.DirRequestFromL2Cache.out_port = network.in_port
        self.L1RequestFromL2Cache = MessageBuffer()
        self.L1RequestFromL2Cache.out_port = network.in_port
        self.responseFromL2Cache = MessageBuffer()
        self.responseFromL2Cache.out_port = network.in_port
        self.unblockToL2Cache = MessageBuffer()
        self.unblockToL2Cache.in_port = network.out_port
        self.L1RequestToL2Cache = MessageBuffer()
        self.L1RequestToL2Cache.in_port = network.out_port
        self.responseToL2Cache = MessageBuffer()
        self.responseToL2Cache.in_port = network.out_port


class DirController(Directory_Controller):
    _version = 0

    @classmethod
    def versionCount(cls):
        cls._version += 1  # Use count for this particular type
        return cls._version - 1

    def __init__(self, ruby_system, ranges, mem_ctrls):
        """ranges are the memory ranges assigned to this controller."""
        # if len(mem_ctrls) > 1:
            # panic("This cache system can only be connected to one mem ctrl")
        super().__init__()
        self.version = self.versionCount()
        self.addr_ranges = ranges
        self.ruby_system = ruby_system
        self.directory = RubyDirectoryMemory()
        # Connect this directory to the memory side.
        self.memory = mem_ctrls[0].port
        self.connectQueues(ruby_system)

    def connectQueues(self, ruby_system):
        self.requestFromCache = MessageBuffer(ordered=True)
        self.requestFromCache.in_port = ruby_system.network.out_port
        self.responseFromCache = MessageBuffer(ordered=True)
        self.responseFromCache.in_port = ruby_system.network.out_port

        self.responseToCache = MessageBuffer(ordered=True)
        self.responseToCache.out_port = ruby_system.network.in_port
        self.forwardToCache = MessageBuffer(ordered=True)
        self.forwardToCache.out_port = ruby_system.network.in_port

       
        self.requestToMemory = MessageBuffer()
        self.responseFromMemory = MessageBuffer()


class IntraChiplet(SimpleNetwork):
    """A simple point-to-point network. This doesn't not use garnet."""

    def __init__(self, ruby_system):
        super().__init__()
        self.netifs = []
        self.ruby_system = ruby_system

    def connectControllers(self, controllers):
        
        self.intra_routers = [Switch(router_id=i) for i in range(len(controllers))]

        
        self.intra_ext_links = [
            SimpleExtLink(link_id=i, ext_node=c, int_node=self.routers[i])
            for i, c in enumerate(controllers)
        ]

        
        link_count = 0
        int_links = []
        for i, ri in enumerate(self.intra_routers):
            for j, rj in enumerate(self.intra_routers):
                if ri == rj:
                    continue  # Don't connect a router to itself!
                if (i / 4 == j / 4):
                    link_count += 1
                    int_links.append(
                        SimpleIntLink(link_id=link_count, src_node=ri, dst_node=rj)
                    )
        self.int_links = int_links

class InterChiplet(GarnetNetwork):


    def __init__(self, ruby_system):
        super().__init__()
        self.netifs = []
        self.ruby_system = ruby_system

    def connectControllers(self, controllers):
        
        self.inter_routers = [GarnetRouter(router_id=i, router_latency=13) for i in range(len(controllers[:16]))]

        # Make a link from each controller to the router. The link goes
        # externally to the network.
        self.inter_ext_links = [
            GarnetExtLink(link_id=i, ext_node=c, int_node=self.routers[i], latency = 12)
            for i, c in enumerate(controllers[:16])
        ]

        
        link_count = 0
        int_links = []
        for i, ri in enumerate(self.inter_routers):
            for j, rj in enumerate(self.inter_routers):
                if ri == rj:
                    continue  
                if (i / 4 == j / 4):
                    link_count += 1
                    int_links.append(
                        GarnetIntLink(link_id=link_count, src_node=ri, dst_node=rj, latency = 12)
                    )
        self.int_links = int_links




