# pull-agent
python3 multi-processing pull agent


```
import fcntl, sys
pid_file = 'program.pid'
fp = open(pid_file, 'w')
try:
    fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    # another instance is running
    sys.exit(0)
```


## poller commands
* poller.stop
* poller.run


# links

https://pymotw.com/3/multiprocessing/basics.html#determining-the-current-process

