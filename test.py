import potsdb
import sys
import random
import time

def normal_test():
	print sys._getframe().f_code.co_name
	t = potsdb.client(HOST, port=PORT)
	for x in range(100):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
	t.wait()
	assert t.queued == 100
		
def slow_test():
	print sys._getframe().f_code.co_name
	t = potsdb.client(HOST, port=PORT, mps=1)
	for x in range(10):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)	
	t.wait()
	assert t.queued == 10
		
def duplicate_test():
	print sys._getframe().f_code.co_name
	t = potsdb.client(HOST, port=PORT)
	for x in range(10):
		t.log('test.metric2', 1, cheese='blue')
	t.wait()
	assert t.queued == 1 # should not queue duplicates

def invalid_metric_test():
	# Attempts to send a metric with invalid name (spaces)
	print sys._getframe().f_code.co_name
	t = potsdb.client(HOST, port=PORT)
	try:
		t.log('test.metric2 roflcopter!', 1, cheese='blue')
	except AssertionError as ex:
		pass
	else:
		raise Exception('should have raised AssertionError for invalid metric')
	assert t.queued == 0
	t.stop()

def timestamp_test():
	# sends many metrics while specifying the timestamp
	print sys._getframe().f_code.co_name
	t = potsdb.client(HOST, PORT)
	ts = int(time.time())
	for x in range(100):
		t.log('test.metric4', 20, tag1='timestamptest', timestamp=ts)
		ts -= 1
	assert t.queued == 100
	t.wait()

def qsize_test(size):
	print sys._getframe().f_code.co_name
	t = potsdb.client(HOST, port=PORT, qsize=size)
	for x in range(5*size):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
	t.wait()
	print "qsize was %s, sent %s" % (size, t.queued)
	assert t.queued >= size

if len(sys.argv) < 3:
	print 'usage: %s host port' % sys.argv[0]
	sys.exit()
	
HOST=sys.argv[1]
PORT=sys.argv[2]

normal_test()
slow_test()
duplicate_test()
invalid_metric_test()
timestamp_test()
qsize_test(100)

print 'done'
