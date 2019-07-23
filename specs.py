#!/usr/bin/env python3

import psutil
import cpuinfo

def main():
    mem = int((psutil.virtual_memory().total /  (1024*1024)))
    swap = int((psutil.swap_memory().total /  (1024*1024)))
    cpu = cpuinfo.get_cpu_info()
    
    print("MEMORY: ")
    print("- Real memory: %uMB" % mem)
    print("- Swap available: %uMB" % swap)
    print("CPU:")
    print("- Cores: %u x %uMHz (%s)" % (cpu['count'], cpu['hz_advertised_raw'][0]/1000000, cpu['brand']))
    print("DISKS:")
    for disk in psutil.disk_partitions():
        if not '/snap' in disk.mountpoint:
            d = psutil.disk_usage(disk.mountpoint)
            print("- %s: %uGB free out of %uGB total" % (disk.mountpoint, d.free/(1024*1024*1024), d.total/(1024*1024*1024)))

    print("NETWORK:")
    ifs = psutil.net_io_counters(pernic=True)
    for net, data in psutil.net_if_addrs().items():
        if not 'AF_INET' in str(data[0].family):
            continue
        print("- %s:" % net)
        for block in data:
            if 'AF_INET' in str(block.family):
                print("  - Protocol = %s, Address = %s, broadcast = %s" %(
                    'IPv6' if 'AF_INET6' in str(block.family) else 'IPv4',
                    block.address,
                    block.broadcast or "??"
                ))
if __name__ == '__main__':
    main()
