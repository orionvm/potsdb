from potsdb import tsdb
import sys
import random


def daemon_test():
	print sys._getframe().f_code.co_name
	t = tsdb(HOST, port=PORT, daemon=True)
	for x in range(100):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
		
def non_daemon_test():
	print sys._getframe().f_code.co_name
	t = tsdb(HOST, port=PORT, daemon=False)
	for x in range(100):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
	
def daemon_slow_test():
	print sys._getframe().f_code.co_name
	t = tsdb(HOST, port=PORT, daemon=True, mps=1)
	for x in range(10):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)	
		
def non_daemon_slow_test():
	print sys._getframe().f_code.co_name
	t = tsdb(HOST, port=PORT, daemon=False, mps=1)
	for x in range(10):
		extratag = str(random.randint(0, 1000000))
		t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)




if len(sys.argv) < 3:
	print 'usage: %s host port' % sys.argv[0]
	sys.exit()
	
HOST=sys.argv[1]
PORT=sys.argv[2]


#daemon_test()
#non_daemon_test()
#daemon_slow_test()
non_daemon_slow_test()
print 'done'