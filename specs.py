#!/usr/bin/env python3

import psutil
import cpuinfo

# FAIL if we don't have at least this:
MINIMUM = {
    'memory': 7200,
    'cpu': 2
}
def pprint(txt = None):
    if not txt:
        txt = '-' * 80
    else:
        txt = txt[:79]
    print("# %-80s #" % txt)

def main():
    mem = int((psutil.virtual_memory().total /  (1024*1024)))
    swap = int((psutil.swap_memory().total /  (1024*1024)))
    cpu = cpuinfo.get_cpu_info()
    
    pprint()
    print("#                        Apache Build System Spec Analyzer                         #")
    pprint()
    
    pprint("MEMORY: ")
    pprint("- Real memory: %uMB" % mem)
    pprint("- Swap available: %uMB" % swap)
    pprint("CPU:")
    pprint("- Cores: %u x %uMHz (%s)" % (cpu['count'], cpu['hz_advertised_raw'][0]/1000000, cpu['brand']))
    pprint("DISKS:")
    for disk in psutil.disk_partitions():
        if not '/snap' in disk.mountpoint:
            d = psutil.disk_usage(disk.mountpoint)
            pprint("- %s: %uGB free out of %uGB total" % (disk.mountpoint, d.free/(1024*1024*1024), d.total/(1024*1024*1024)))

    pprint("NETWORK:")
    ifs = psutil.net_io_counters(pernic=True)
    for net, data in psutil.net_if_addrs().items():
        if not 'AF_INET' in str(data[0].family):
            continue
        pprint("- %s:" % net)
        for block in data:
            if 'AF_INET' in str(block.family):
                pprint("  - Protocol = %s, Address = %s, broadcast = %s" %(
                    'IPv6' if 'AF_INET6' in str(block.family) else 'IPv4',
                    block.address,
                    block.broadcast or "??"
                ))
    
    pprint()
    if cpu['count'] < MINIMUM['cpu'] or mem < MINIMUM['memory']:
        pprint("Machine does not meet minimum requirements for Apache!\n")
        pprint()
        sys.exit(-1)
    else:
        pprint('System meets Apache build standards')
        pprint()

if __name__ == '__main__':
    main()
