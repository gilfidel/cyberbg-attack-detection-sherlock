#encoding: utf-8

import re

description_from_pdf = """ userid [string]: the user ID to whom this sample belongs to.
 uuid [int]: Unix timestamp in milliseconds of when this event occurred.
 applicationname [string]: The name of the sampled application described in this record.
 cpu_usage [double]: The percent of CPU utilization normalized to a constant CPU clock speed. Note that this
data field has been depreciated. It is recommended to use the stime, utime, cstime, cutime fields to measure
the app’s activity.
 packagename [string]: The Android package name of this app (e.g., com.example.helloandroid)
 packageuid [int]: The UID identifier of this app’s package.
 uidrxbytes [int]: Bytes received by this application since the last time the T4 probe was activated (approximately
5 seconds on average –compare uuids for accuracy). If this is the first sample since boot, then the value is -1.
 uidrxpackets [int]: Packets received by this application since the last time the T4 probe was activated
(approximately 5 seconds on average –compare uuids for accuracy). If this is the first sample since boot, then
the value is -1. uidtxbytes [int]: Bytes transmitted by this application since the last time the T4 probe was activated
(approximately 5 seconds on average –compare uuids for accuracy). If this is the first sample since boot, then
the value is -1.
 uidtxpackets [int]: Packets transmitted by this application since the last time the T4 probe was activated
(approximately 5 seconds on average –compare uuids for accuracy). If this is the first sample since boot, then
the value is -1.
 cguest_time [int]: Guest time of the process's children, measured in clock ticks.
 cmaj_flt [int]: The number of major faults that the process's waited-for children have made.
 cstime [int]: Amount of time that this process's waited-for children have been scheduled in kernel mode,
measured in clock ticks.
 cutime [int]: Amount of time that this process's waited-for children have been scheduled in user mode,
measured in clock ticks. This includes guest time, cguest_time (time spent running a virtual CPU).
 dalvikprivatedirty [int]: The private dirty pages used by dalvik heap.
 dalvikpss [int]: The proportional set size for dalvik heap.
 dalvikshareddirty [int]: The shared dirty pages used by dalvik heap.
 guest_time [int]: Guest time of the process (time spent running a virtual CPU for a guest operating system),
measured in clock ticks.
 importance [int]: The relative importance level that the system places on this process (details). For example,
background, foreground, service, sleeping, …etc.
 importancereasoncode [int]: The reason for importance, if any (details).
 importancereasonpid [int]: For the specified values of importanceReasonCode, this is the process ID of the
other process that is a client of this process (details).
 lru [int]: An additional ordering within a particular Android importance category, providing finer-grained
information about the relative utility of processes within a category (details).
 nativeprivatedirty [int]: The private dirty pages used by the native heap.
 nativepss [int]: The proportional set size for the native heap.
 nativeshareddirty [int]: The shared dirty pages used by the native heap.
 num_threads [int]: Number of threads in this process.
 otherprivatedirty [int]: The private dirty pages used by everything else.
 otherpss [int]: The proportional set size for everything else.
 othershareddirty [int]: The shared dirty pages used by everything else.
 pgid [int]: ]: The ID of the foreground process group of the process.
 pid [int]: The process ID of this process.
 ppid [int]: The PID of parent process.
 priority [int]: (Explanation for Linux 2.6) For processes running a real-time scheduling policy (policy below; see
sched_setscheduler(2)), this is the negated scheduling priority, minus one; that is, a number in the range -2 to -
100, corresponding to real-time priorities 1 to 99. For processes running under a non-real-time scheduling
policy, this is the raw nice value (setpriority(2)) as represented in the kernel. The kernel stores nice values as
numbers in the range 0 (high) to 39 (low), corresponding to the user-visible nice range of -20 to 19.
 rss [int]: Resident Set Size: number of pages the process has in real memory. This is just the pages which count
toward text, data, or stack space. This does not include pages which have not been demand-loaded in, or which
are swapped out.
 rsslim [int]: Current soft limit in bytes on the rss of the process.
 sid [int]: The process’s session ID.
 start_time [int]: The time the process started after system boot. In kernels before Linux 2.6, this value was
expressed in jiffies. Since Linux 2.6, the value is expressed in clock ticks.
 state [string]: Current state of the process. One of "R (running)", "S (sleeping)", "D (disk sleep)", "T (stopped)",
"T (tracing stop)", "Z (zombie)", or "X (dead)". stime [int]: Amount of time that this process has been scheduled in kernel mode, measured in clock ticks.
 tcomm [string]: An associated string with the executable’s name.
 utime [int]: Amount of time that this process has been scheduled in user mode, measured in clock ticks. This
includes guest time, guest_time (time spent running a virtual CPU, see below), so that applications that are not
aware of the guest time field do not lose that time from their calculations.
 vsize [int]: Virtual memory size in bytes.
 version_code [int]: An integer used as an internal version number for the Android app. This number is used only
to determine whether one version is more recent than another, with higher numbers indicating more recent
versions. This is not the version number shown to users (details).
 version_name [string]: A string used as the version number shown to users. This setting can be specified as a
raw string or as a reference to a string resource.
 sherlock_version [string]: The current version of the SherLock collection agent running on the device.
 tgpid [int]: The ID of the foreground process group of the controlling terminal of the process. -1 if the process is
not connected to a terminal.
 Flags [string]: the internal kernel flags holding the status of the socket (e.g., 00010000).
 Wchan [string]: This is the "channel" in which the process is waiting. It is the address of a location in the kernel
where the process is sleeping. The corresponding symbolic name can be found in /proc/[pid]/wchan.
 exit_signal [int]: Signal to be sent to parent when we die.
 minflt [int]: The number of minor faults the process has made which have not required loading a memory page
from disk.
 cminflt [int]: The number of minor faults that the process's waited-for children have made.
 majflt [int]: The number of major faults the process has made which have required loading a memory page from
disk.
 startcode [int]: The address above which program text can run.
 endcode [int]: The address below which program text can run.
 nice [int]: The nice value a value in the range 19 (low priority) to -20 (high priority).
 Itrealvalue [int]: The time in jiffies before the next SIGALRM is sent to the process due to an interval timer.
Since kernel 2.6.17, this field is no longer maintained, and is hard coded as 0.
 Processor [int]: CPU number last executed on.
 rt_priority [int]: Real-time scheduling priority, a number in the range 1 to 99 for processes scheduled under a
real-time policy, or 0, for non-real-time processes."""

csv_header = 'UserId,UUID,ApplicationName,CPU_USAGE,PackageName,PackageUID,UidRxBytes,UidRxPackets,UidTxBytes,UidTxPackets,cguest_time,cmaj_flt,cstime,cutime,dalvikPrivateDirty,dalvikPss,dalvikSharedDirty,guest_time,importance,importanceReasonCode,importanceReasonPid,lru,nativePrivateDirty,nativePss,nativeSharedDirty,num_threads,otherPrivateDirty,otherPss,otherSharedDirty,pgid,pid,ppid,priority,rss,rsslim,sid,start_time,state,stime,tcomm,utime,vsize,Version_Code,Version_Name,sherlock_version,tgpid,flags,wchan,exit_signal,minflt,cminflt,majflt,startcode,endcode,nice,itrealvalue,processor,rt_priority'

def _get_type(t):
    return {
        'string' : 'str',
        'int' : "'Int64'",
        'bool' : "'Int64'",
        'double' : 'numpy.float64',
    }[t.lower()]

fields_from_csv = [x.lower().strip() for x in csv_header.split(',')]
fields_and_types = re.findall( r'\uf0b7\s*(\w+)\s*\[(\w+)\]', description_from_pdf, re.MULTILINE)

print(f'{len(fields_from_csv)} fields total.')

fields_and_types = dict([(name.lower(), _get_type(t)) for (name, t) in fields_and_types ])

print('[' + ', '.join(f'("{name}", {fields_and_types[name]}, True)' for name in fields_from_csv)+ ']')
