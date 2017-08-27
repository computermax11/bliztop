#!/usr/bin/env python
import sys
from bliztop import * 

def main():
    if len(sys.argv) == 1:
       sys.exit('use  bliztop <NAME>  or  bliztop <PID>') 
    else:
        pollcycle(sys.argv[1:])

if __name__ == "__main__":
    main()
