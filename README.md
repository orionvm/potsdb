potsdb
======

Python client to OpenTSDB

This was designed with a long running parent program in mind, where sending metrics was something that happens on the side.
Implemented such that sending the metric "put" message to the Time Series Database API does not block the calling application. This is achieved by creating a background worker thread which takes metrics off the Queue, then sending them on a TCP socket to HOST. The client.log method simply sets up and puts the metric on the Queue, then returns.

When the client object is instantiated, a temporary socket is created to the target HOST, PORT combination to check for connectivity. This may fail with a timeout error. However if the background thread encounters socket communication problems like timeout further down the line (in the sending metrics loop) then it will silenty keep trying to reconnect forever.

Keep in mind that if you send a bunch of metrics through .log then immediately quit, the background thread will also terminate, without having had enough time to send your metrics properly.

Rate limiting for sending metrics over TCP is by default set to 100 Metrics Per Second. This can be overwritten upon instantiation.

Installation
===
Clone this repo, then 
```
cd potsdb
python setup.py install
```
or
```
pip install potsdb
```

Usage
===
```
import potsdb

# minimum is hostname. port is defaulted to 4242:
metrics = potsdb.Client('hostname.local')
# all options:
metrics = potsdb.Client('hostname.local', port=4242, qsize=1000, host_tag=True, mps=100, check_host=True)

# qsize: Max Size of Queue
# host_tag: True for automatic, string value for override, None for nothing
# mps: Metrics Per Second rate limiting
# check_host: change to false to skip startup connectivity checking

# Bare minimum is metric name, metric value
metrics.send('test.metric2', 100)
# tags can also be specified
metrics.send('test.metric5', 100, extratag1='tagvalue', extratag2='tagvalue')
# host tag is set automatically, but can be overwritten
metrics.send('test.metric6', 34, host='app1.local')

# waits for all outstanding metrics to be sent and background thread closes
metrics.wait()

```
