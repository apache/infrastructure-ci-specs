#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

""" ASF CI spec analyzer """

import psutil
import cpuinfo
import sys

# FAIL if we don't have at least this:
MINIMUM = {
    'memory': 7200,
    'cpu': 2,
    'ROOTDISK': 40,
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
    rootdisk = 0
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
            if disk.mountpoint == '/':
                rootdisk = d.free/(1024*1024*1024)

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
    pprint("RESULTS:")
    failed = False
    if cpu['count'] < MINIMUM['cpu']:
        pprint(u"✗ FAIL: CPU count is %u, expected at least %u!" % (cpu['count'], MINIMUM['cpu']))
        failed = True
    else:
        pprint(u'✓ PASS: CPU count is %u, minimum requirement is %u.' % (cpu['count'], MINIMUM['cpu']))
        
    if mem < MINIMUM['memory']:
        pprint(u"✗ FAIL: Memory available is %uMB, expected at least %uMB!" % (mem, MINIMUM['memory']))
        failed = True
    else:
        pprint(u'✓ PASS: Memory is %uMB, minimum requirement is %uMB.' % (mem, MINIMUM['memory']))
    
    if rootdisk < MINIMUM['ROOTDISK']:
        pprint(u"✗ FAIL: Root (/) partition has %uGB free space, expected at least %uGB!" % (rootdisk, MINIMUM['ROOTDISK']))
        failed = True
    else:
        pprint(u'✓ PASS: Root (/) partition has %uGB free space, minimum requirement is %uGB.' % (rootdisk, MINIMUM['ROOTDISK']))

    
    if failed:
        pprint(u"✗ FAIL: Machine does not meet minimum requirements for Apache!\n")
        pprint()
        sys.exit(-1)
    else:
        pprint(u'✓ PASS: System meets Apache build standards')
        pprint()

if __name__ == '__main__':
    main()
