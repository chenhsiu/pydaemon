Daemon Start
==

```
$ ./amz_crawlerd.py start
```
Daemon Stop
==

```
$ ./amz_crawlerd.py stop
```

or

```
kill `cat run/amz_crawlerd.pid`
```

Graceful Shutdown
==

Kill the daemon with SIGINT (-2) to notify

```
$ kill -2 `cat run/amz_crawlerd.pid`
$ tail log/amz_crawlerd.out
running 0
running 1
running 2
running 3
running 4
running 5
running 6
running 7
Interrupt on signal 2
graceful shutdown
```

