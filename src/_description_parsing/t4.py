#encoding: utf-8

import re

description_from_pdf = """ userid [string]: the user ID to whom this sample belongs to.
 uuid [int]: Unix timestamp in milliseconds of when this event occurred.
 version [string]: The current version of the SherLock collection agent running on the device.
 traffic_mobilerxbytes [int]: Number of Bytes received over mobile data since the last activation of the T4 probe
(a value of -1 indicates that this is the first sample since boot). traffic_mobilerxpackets [int]: Number of Packets received over mobile data since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_mobiletxbytes [int]: Number of Bytes transmitted over mobile data since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_mobiletxpackets [int]: Number of Packets transmitted over mobile data since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_totalrxbytes [int]: Number of Bytes received over all networks since the last activation of the T4 probe (a
value of -1 indicates that this is the first sample since boot).
 traffic_totalrxpackets [int]: Number of Packets received over all networks since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_totaltxbytes [int]: Number of Bytes transmitted over all networks since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_totaltxpackets [int]: Number of Packets transmitted over all networks since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_totalwifirxbytes [int]: Number of Bytes received over Wi-Fi since the last activation of the T4 probe (a
value of -1 indicates that this is the first sample since boot).
 traffic_totalwifirxpackets [int]: Number of Packets received over all networks since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_totalwifitxbytes [int]: Number of Bytes transmitted over Wi-Fi since the last activation of the T4 probe (a
value of -1 indicates that this is the first sample since boot).
 traffic_totalwifitxpackets [int]: Number of Packets transmitted over Wi-Fi since the last activation of the T4
probe (a value of -1 indicates that this is the first sample since boot).
 traffic_timestamp [string]: DateTime indicating when the traffic was calculated.
 battery_charge_type [int]: A value indicating the method of charging.
 battery_current_avg [int]: Average battery current in microamperes, as an integer. Positive values indicate net
current entering the battery from a charge source, negative values indicate net current discharging from the
battery. The time period over which the average is computed may depend on the fuel gauge hardware and its
configuration.
 battery_health [int]: A value that indicated the current health of the battery (e.g., good, hot, over voltage,…)
 battery_icon_small [int]: The resource ID of a small status bar icon indicating the current battery state
 battery_invalid_charger [int]: Indication if the charger is invalid.
 battery_level [int]: The current battery level (0-100)
 battery_online [bool]: An indication if the battery is operational.
 battery_plugged [bool]: An indication if the battery is plugged in.
 battery_present [string]: An indication if the battery is in the device.
 battery_scale [int]: The maximum battery level.
 battery_status [int]: the current status constant.
 battery_technology [string]: The technology of the current battery.
 battery_temperature [int]: The current battery temperature in tenths of a degree Centigrade.
 battery_timestamp [string]: A DateTime indicating when the battery statistics were sampled.
 battery_voltage [int]: current battery voltage in millivolts.
 cpuhertz [int]: the current clock speed of the CPU taken from
proc/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
 cpu_0 [int]: CPU utilization of core #0 in percentage.
 cpu_1 [int]: CPU utilization of core #1 in percentage.
 cpu_2 [int]: CPU utilization of core #2 in percentage.
 cpu_3 [int]: CPU utilization of core #3 in percentage.
 total_cpu [int]: Total CPU utilization in percentage. totalmemory_freesize [int]: Memory free in the Android heap.
 totalmemory_max_size [int]: Max memory avalaible in the Android heap.
 totalmemory_total_size [int]: Total memory in the Android heap.
 totalmemory_used_size [int]: Total memory used in the Android heap.
 memtotal [int]: Total amount of usable RAM, in kibibytes, which is physical RAM minus a number of reserved
bits and the kernel binary code.
 Memfree [int]: The amount of physical RAM, in kibibytes, left unused by the system.
 buffers [int]: The amount, in kibibytes, of temporary storage for raw disk blocks.
 cached [int]: The amount of physical RAM, in kibibytes, used as cache memory.
 swapcached [int]: The amount of memory, in kibibytes, that has once been moved into swap, then back into the
main memory, but still also remains in the swapfile. This saves I/O, because the memory does not need to be
moved into swap again.
 active [int]: The amount of memory, in kibibytes, that has been used more recently and is usually not reclaimed
unless absolutely necessary.
 inactive [int]: The amount of memory, in kibibytes, that has been used less recently and is more eligible to be
reclaimed for other purposes.
 active_anon [int]: The amount of anonymous and tmpfs/shmem memory, in kibibytes, that is in active use, or
was in active use since the last time the system moved something to swap.
 inactive_anon [int]: The amount of anonymous and tmpfs/shmem memory, in kibibytes, that is a candidate for
eviction.
 active_file [int]: The amount of file cache memory, in kibibytes, that is in active use, or was in active use since
the last time the system reclaimed memory.
 inactive_file [int]: The amount of file cache memory, in kibibytes, that is newly loaded from the disk, or is a
candidate for reclaiming.
 unevictable [int]: The amount of memory, in kibibytes, discovered by the pageout code, that is not evictable
because it is locked into memory by user programs.
 mlocked [int]: The total amount of memory, in kibibytes, that is not evictable because it is locked into memory
by user programs.
 hightotal [int]: The total amount of memory, in kilobytes, that is not directly mapped into kernel space.
 highfree [int]: The free memory, in kilobytes, that is not directly mapped into kernel space.
 lowtotal [int]: The total amount of memory, in kilobytes, that is directly mapped into kernel space.
 lowfree [int]: The free memory, in kilobytes, that is directly mapped into kernel space.
 swaptotal [int]: The total amount of swap available, in kibibytes.
 swapfree [int]: The total amount of swap free, in kibibytes.
 dirty [int]: The total amount of memory, in kibibytes, waiting to be written back to the disk.
 writeback [int]: The total amount of memory, in kibibytes, actively being written back to the disk.
 anonpages [int]: The total amount of memory, in kibibytes, used by pages that are not backed by files and are
mapped into userspace page tables.
 mapped [int]: The memory, in kibibytes, used for files that have been mmaped, such as libraries.
 shmem [int]: The total amount of memory, in kibibytes, used by shared memory (shmem) and tmpfs.
 slab [int]: The total amount of memory, in kibibytes, used by the kernel to cache data structures for its own use.
 sreclaimable [int]: The part of Slab that can be reclaimed, such as caches.
 sunreclaim [int]: The part of Slab that cannot be reclaimed even when lacking memory.
 kernelstack [int]: The amount of memory, in kibibytes, used by the kernel stack allocations done for each task in
the system.
 pagetables [int]: The total amount of memory, in kibibytes, dedicated to the lowest page table level.
 commitlimit [int]: The total amount of memory currently available to be allocated on the system based on the
overcommit ratio. committed_as [int]: The total amount of memory, in kibibytes, estimated to complete the workload. This value
represents the worst case scenario value, and also includes swap memory.
 vmalloctotal [int]: The total amount of memory, in kibibytes, of total allocated virtual address space.
 vmallocused [int]: The total amount of memory, in kibibytes, of used virtual address space.
 vmallocchunk [int]: The largest contiguous block of memory, in kibibytes, of available virtual address space.
 msmgpio_cpu0 [int]: Accumulative interrupts for the msmgpio component. Interrupts on CPU #0.
 msmgpio_sum_cpu123 [int]: Accumulative interrupts for the msmgpio component. Interrupts on CPUs #1, #2,
#3.
 wcd9xxx_cpu0 [int]: Accumulative interrupts for the wcd9xxx component. Interrupts on CPU #0.
 wcd9xxx_sum_cpu123 [int]: Accumulative interrupts for the wcd9xxx component. Interrupts on CPUs #1, #2, #3.
 pn547_cpu0 [int]: Accumulative interrupts for the pn547component. Interrupts on CPU #0.
 pn547_sum_cpu123 [int]: Accumulative interrupts for the pn547component. Interrupts on CPUs #1, #2, #3.
 cypress_touchkey_cpu0 [int]: Accumulative hardware interrupt count of back button presses. Interrupts on CPU
#0.
 cypress_touchkey_sum_cpu123 [int]: Accumulative hardware interrupt count of back button presses. Interrupts
on CPUs #1, #2, #3.
 synaptics_rmi4_i2c_cpu0 [int]: Accumulative hardware interrupt count for the touch screen (a single gesture
may incur many interrupts –e.g., x y coordinate change). Interrupts on CPU #0.
 synaptics_rmi4_i2c_sum_cpu123 [int]: Accumulative hardware interrupt count for the touch screen (a single
gesture may incur many interrupts –e.g., x y coordinate change). Interrupts on CPUs #1, #2, #3.
 sec_headset_detect_cpu0 [int]: Accumulative hardware interrupt count for head set detection. Interrupts on
CPU #0.
 sec_headset_detect_sum_cpu123 [int]: Accumulative hardware interrupt count for head set detection.
Interrupts on CPUs #1, #2, #3.
 flip_cover_cpu0 [int]: Accumulative hardware interrupt count for head set detection. Interrupts on CPU #0.
 flip_cover_sum_cpu123 [int]: Accumulative hardware interrupt count for head set detection. Interrupts on CPUs
#1, #2, #3.
 home_key_cpu0 [int]: Accumulative hardware interrupt count of home key presses. Interrupts on CPU #0.
 home_key_sum_cpu123 [int]: Accumulative hardware interrupt count of home key presses. Interrupts on CPUs
#1, #2, #3.
 volume_down_cpu0 [int]: Accumulative hardware interrupt count of volume down button presses. Interrupts
on CPU #0.
 volume_down_sum_cpu123 [int]: Accumulative hardware interrupt count of volume down button presses.
Interrupts on CPUs #1, #2, #3.
 volume_up_cpu0 [int]: Accumulative hardware interrupt count of volume up button presses. Interrupts on CPU
#0.
 volume_up_sum_cpu123 [int]: Accumulative hardware interrupt count of volume up button presses. Interrupts
on CPUs #1, #2, #3.
 companion_cpu0 [int]: Accumulative hardware interrupt count of companion occurrences. Interrupts on CPU
#0.
 companion_sum_cpu123 [int]: Accumulative hardware interrupt count of companion occurrences. Interrupts on
CPUs #1, #2, #3.
 slimbus_cpu0 [int]: Accumulative interrupt count on the slimbus. Interrupts on CPU #0.
 slimbus_sum_cpu123 [int]: Accumulative interrupt count on the slimbus. Interrupts on CPUs #1, #2, #3.
 function_call_interrupts_cpu0 [int]: Accumulative software interrupt count on function calls. Interrupts on CPU
#0.
 function_call_interrupts_sum_cpu123 [int]: Accumulative software interrupt count on function calls. Interrupts
on CPUs #1, #2, #3. cpu123_intr_prs [int]: Accumulative interrupt count on the intr_prs element.
 tot_user [int]: The number of normal processes executing in user mode.
 tot_nice [int]: The number of niced processes executing in user mode.
 tot_system [int]: The number of processes executing in kernel mode.
 tot_idle [int]: The number of twiddling thumbs.
 tot_iowait [int]: The number of waiting for I/O to complete.
 tot_irq [int]: The number of servicing interrupts.
 tot_softirq [int]: The number of servicing softirqs.
 ctxt [int]: The total number of context switches across all CPUs.
 btime [int]: The time at which the system booted, in seconds since the Unix epoch.
 processes [int]: The number of processes and threads created, which includes (but is not limited to) those
created by calls to the fork() and clone() system calls.
 procs_running [int]: The number of processes currently running on CPUs.
 procs_blocked [int]: The number of processes currently blocked, waiting for I/O to complete.
 connectedwifi_ssid [int]: The salted hash of the connected Wi-Fi access point’s SSID.
 connectedwifi_level [int]: The reception level of the connected Wi-Fi access point (RSSI).
 internal_availableblocks [int]: Avalaible blocks in internal storage.
 internal_blockcount [int]: Number of blocks in internal storage.
 internal_freeblocks [int]: Free blocks in internal storage.
 internal_blocksize [int]: Block size in internal storage.
 internal_availablebytes [int]: Avalaible Bytes in internal storage.
 internal_freebytes [int]: Free Bytes in internal storage.
 internal_totalbytes [int]: Total Bytes in external (SD card) storage.
 external_availableblocks [int]: Avalaible blocks in external (SD card) storage.
 external_blockcount [int]: Number of blocks in external (SD card) storage.
 external_freeblocks [int]: Number of blocks in external (SD card) storage.
 external_blocksize [int]: Block size in external (SD card) storage.
 external_availablebytes [int]: Avalaible Bytes in external (SD card) storage.
 external_freebytes [int]: Free Bytes in external (SD card) storage.
 external_totalbytes [int]: Total Bytes in external (SD card) storage.
"""

csv_header = r'''Userid,UUID,Version,CpuHertz,CPU_0,CPU_1,CPU_2,CPU_3,Total_CPU,TotalMemory_freeSize,TotalMemory_max_size,TotalMemory_total_size,TotalMemory_used_size,Traffic_MobileRxBytes,Traffic_MobileRxPackets,Traffic_MobileTxBytes,Traffic_MobileTxPackets,Traffic_TotalRxBytes,Traffic_TotalRxPackets,Traffic_TotalTxBytes,Traffic_TotalTxPackets,Traffic_TotalWifiRxBytes,Traffic_TotalWifiRxPackets,Traffic_TotalWifiTxBytes,Traffic_TotalWifiTxPackets,Traffic_timestamp,Battery_charge_type,Battery_current_avg,Battery_health,Battery_icon_small,Battery_invalid_charger,Battery_level,Battery_online,Battery_plugged,Battery_present,Battery_scale,Battery_status,Battery_technology,Battery_temperature,Battery_timestamp,Battery_voltage,MemTotal,MemFree,Buffers,Cached,SwapCached,Active,Inactive,Active_anon,Inactive_anon,Active_file,Inactive_file,Unevictable,Mlocked,HighTotal,HighFree,LowTotal,LowFree,SwapTotal,SwapFree,Dirty,Writeback,AnonPages,Mapped,Shmem,Slab,SReclaimable,SUnreclaim,KernelStack,PageTables,CommitLimit,Committed_AS,VmallocTotal,VmallocUsed,VmallocChunk,msmgpio_cpu0,msmgpio_sum_cpu123,wcd9xxx_cpu0,wcd9xxx_sum_cpu123,pn547_cpu0,pn547_sum_cpu123,cypress_touchkey_cpu0,cypress_touchkey_sum_cpu123,synaptics_rmi4_i2c_cpu0,synaptics_rmi4_i2c_sum_cpu123,sec_headset_detect_cpu0,sec_headset_detect_sum_cpu123,flip_cover_cpu0,flip_cover_sum_cpu123,home_key_cpu0,home_key_sum_cpu123,volume_down_cpu0,volume_down_sum_cpu123,volume_up_cpu0,volume_up_sum_cpu123,companion_cpu0,companion_sum_cpu123,SLIMBUS_cpu0,SLIMBUS_sum_cpu123,function_call_interrupts_cpu0,function_call_interrupts_sum_cpu123,cpu123_intr_prs,tot_user,tot_nice,tot_system,tot_idle,tot_iowait,tot_irq,tot_softirq,ctxt,btime,processes,procs_running,procs_blocked,connectedWifi_SSID,connectedWifi_Level'''

def _get_type(t):
    return {
        'string' : 'str',
        'int' : "'Int64'",
        'bool' : "'Int64'"
    }[t.lower()]

fields_from_csv = [x.lower().strip() for x in csv_header.split(',')]
fields_and_types = re.findall( r'\uf0b7\s*(\w+)\s*\[(\w+)\]', description_from_pdf, re.MULTILINE)

print(f'{len(fields_from_csv)} fields total.')

fields_and_types = dict([(name.lower(), _get_type(t)) for (name, t) in fields_and_types ])

#fixes due to de-facto info as seen in T4.tsv
fields_and_types['cpuhertz'] = 'str'
fields_and_types['cpu_0'] = 'numpy.float32'
fields_and_types['cpu_1'] = 'numpy.float32'
fields_and_types['cpu_2'] = 'numpy.float32'
fields_and_types['cpu_3'] = 'numpy.float32'
fields_and_types['total_cpu'] = 'numpy.float32'


print('[' + ', '.join(f'("{name}", {fields_and_types[name]}, True)' for name in fields_from_csv)+ ']')
