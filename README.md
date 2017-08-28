# bliztop

## Blizzard Senior Linux Administrator Code Challenge ##

* Design a simple implementation of top that you can run to query for information about the processes running on the system.
* Your version of top must allow you to specify a pid or regex of process names on which to display information
* It must display information about memory usage, cpu usage, owner, and the process name
* It must query for this information on intervals of 5 seconds or less and print a summary of the information to the screen twice per minute. This summary information should be an average of the interval after it was last printed

---
## Install ##
The program can be installed using python setuptools.
```python setup.py install```
If you don't want to install it, the script can be run by executing bliztop.py in the bliztop folder
```python bliztop/bliztop.py```

## Use ##
```bliztop <pid>```
or
```bliztop <name>```
you can use multiple pids or names or a combination of both.
processes which die will be removed and new processes that match a PID or regex will be added (may take a cycle)

## Settings ##
The program is configured to poll at 2 second intervals and display the results twice per minute, this can be changed
by modifying bliztop.py

### Compatibility ###
The script should work with version 2 or 3 of python ( tested 2.7 and 3.5 )
