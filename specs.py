#!/usr/bin/env python3

import psutil

def main():
    mem = int((psutil.virtual_memory().total /  (1024*1024)))
    swap = int((psutil.swap_memory().total /  (1024*1024)))
    cpu = psutil.cpu_freq(percpu = True)
    
    print("Memory available: %uMB" % mem)
    print("Swap available: %uMB" % swap)
    print("Cores: %u x %uMHz" % (len(cpu), cpu[0].max))
    
    for disk in psutil.disk_partitions():
        if not '/snap' in disk.mountpoint:
            d = psutil.disk_usage(disk.mountpoint)
            print("%s: %uGB free out of %uGB total" % (disk.mountpoint, d.free/(1024*1024*1024), d.total/(1024*1024*1024)))


if __name__ == '__main__':
    main()
