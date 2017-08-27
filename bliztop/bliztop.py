#!/usr/bin/env python3
#  Blizzard Advanced Systems Administrator Code Challenge
#  Max Schulberg
import time
import sys
import re
import os
from psutil import cpu_times, Process, pid_exists, process_iter
from statistics import mean

template = "{0:<8}|{1:<24}|{2:<12}|{3:>8.2f}%|{4:>7.0f}M|" 
htemplate = "{0:8}|{1:24}|{2:12}|{3:8}%|{4:8}|"
cycle = 5

MB = lambda x: x * 9.5367431640625E-7

class Proc(object):
    def __init__(self, pid):
        self.pid = pid
        self.proc = Process(pid)
        with self.proc.oneshot():
            self.name = self.proc.name()
            self.owner = self.proc.username()
            self.created = self.proc.create_time()
    def poll(self, delay=1):
        if not self.proc.is_running():
            return ( self.pid, self.name + "**DEAD**", '', 0, 0 )
        with self.proc.oneshot():
            self.poll1 = self.proc.cpu_times()
            self.virtual1 = self.proc.memory_info().vms
        self.system1 = cpu_times()
        time.sleep(delay)
        with self.proc.oneshot():
            self.poll2 = self.proc.cpu_times()
            self.virtual2 = self.proc.memory_info().vms
        self.system2 = cpu_times()
        self.proc_time = sum(self.poll2) - sum(self.poll1)
        self.cpu_time = sum(self.system2) - sum(self.system1)
        self.virtual = MB(( self.virtual1 + self.virtual2 ) / 2)
        self.cpu_percent = 100 * ( self.proc_time / self.cpu_time ) 
        return ( self.pid, self.name, self.owner, self.cpu_percent, self.virtual )
    def is_running(self):
        return self.proc.is_running()
    def __repr__(self):
        return "**process** %s (%d)" % ( self.proc.name(), self.pid )
    def __str__(self):
        return template.format(self.pid, self.name, self.owner, self.cpu_percent, self.virtual)

def print_header():
    os.system('clear')
    print(htemplate.format("PID", "NAME", "OWNER", "CPU", "MEM"))

def iter_pids(args):
    regex = ''
    for arg in args:
        if re.match(r'^[0-9]+$', arg) and pid_exists(int(arg)): yield int(arg)
        else:
            regex += '%s|' % arg   
    for p in process_iter():
        if Process().pid == p.pid: pass
        elif re.search(regex[:-1], ' '.join(p.cmdline())): yield p.pid

def tally(resultlist, field):
    return round(mean([x[field] for x in resultlist]), 1)

def pollcycle(args, cyclelength=cycle):
    print('Please wait while initial data is gathered.  Ctrl-C to exit.')
    procs = [Proc(pid) for pid in iter_pids(args)]
    results = {p.pid: [] for p in procs}
    while True: # MAIN LOOP
        start = time.time()
        while time.time() < ( start + cyclelength ):
            for proc in procs:
                results[proc.pid].append(proc.poll())
        print_header()
        for proc in procs:  # no sort
            print(template.format(proc.pid, proc.name, proc.owner, tally(results[proc.pid], 3), tally(results[proc.pid],4)))
            results[proc.pid] = [results[proc.pid][-1]] # keep only the last poll in results, so it doesn't drop back to 0 or get huge

def main():
    if len(sys.argv) == 1:
        sys.exit('use  bliztop <NAME>  or  bliztop <PID>')
    pollcycle(sys.argv[1:])


if __name__ == "__main__":
    main()
