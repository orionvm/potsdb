import socket
import time
import Queue
import threading
import time
import random

MPS_LIMIT = 100

_last_timestamp = None
_last_metrics = set()

def _mksocket(host, port, q, done):
	"""Returns a tcp socket to (host/port). Retries forever every 5 seconds if connection fails"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while 1:
		try:
			s.connect((host, port))	
			return s
		except:
			# retry connection forever, as long as parent is still alive
			assert not done.is_set(), "Failed to connect to tsdb server"
			time.sleep(5)


def _push(host, port, q, done, mps):
	"""Worker thread. Connect to host/port, pull data from q until done is set"""

	sock = None
	retry_line = None
	while 1:
		stime = time.time()

		if sock == None:
			sock = _mksocket(host, port, q, done)

		if retry_line:
			line = retry_line
			retry_line = None
		else:
			try:
				line = q.get(True, 1) # blocking, with 1 second timeout
			except:
				if done.is_set(): # no items in queue, and parent finished
					break
				else: # no items in queue, but parent might send more
					continue

		try:
			sock.send(line)
		except:
			sock = None # notify that we need to make a new socket at start of loop
			retry_line = line # can't really put back in q, so remember to retry this line
			continue

		etime = time.time() - stime #time that actually elapsed

		#Expected value of wait_time is 1/MPS_LIMIT, ie. MPS_LIMIT per second.
		wait_time = (2.0 * random.random()) / (mps)
		if wait_time > etime: #if we should wait
			time.sleep(wait_time - etime) #then wait


	if sock:
		sock.close()

class tsdb():

	def __init__(self, host, port=4242, qsize=1000, host_tag=True, daemon=False, mps=MPS_LIMIT):
		"""Main tsdb client. Connect to host/port. Buffer up to qsize metrics"""

		self.q = Queue.Queue(maxsize=qsize)
		self.done = threading.Event()
		self.t = threading.Thread(target=_push, args = (host, int(port), self.q, self.done, mps))
		self.t.daemon = daemon
		self.host = host
		self.port = port
		
		if host_tag == True:
			self.host_tag = socket.gethostname()
		elif isinstance(host_tag, str):
			self.host_tag = host_tag
			
		self.t.start()

	def log(self, name, val, **tags):
		"""Log metric name with value val. You must include at least one tag as a kwarg"""
		global _last_timestamp, _last_metrics
		
		val = float(val) #Duck type to float/int, if possible.
		if int(val) == val:
			val = int(val)

		if self.host_tag and 'host' not in tags:
			tags['host'] = self.host_tag

		# get timestamp from system time, unless it's supplied as a tag
		timestamp = int(tags.pop('timestamp', time.time()))

		assert not self.done.is_set(), "Connection closed!"
		assert tags != {}, "Need at least one tag"
		
		tagvals = ' '.join(['%s=%s' % (k,v) for k,v in tags.items()])
		
		# OpenTSDB has major problems if you insert a data point with the same
		# metric, timestamp and tags. So we keep a temporary set of what points
		# we have sent for the last timestamp value. If we encounter a duplicate, 
		# it is dropped.
		unique_str = name + str(timestamp) + tagvals + self.host + str(self.port)
		if timestamp == _last_timestamp or _last_timestamp == None:
			if unique_str in _last_metrics:
				return # discard duplicate metrics
			else:
				_last_metrics.add(unique_str)
		else:
			_last_timestamp = timestamp
			_last_metrics.clear()
		
		line = "put %s %d %d %s\n" % (name, timestamp, val, tagvals)

		try:
			self.q.put(line, False)
		except Queue.Full:
			self.q.get() #Drop the oldest metric to make room
			self.q.put(line, False)
	
	def close(self):
		"""Close and clean up the connection"""
		self.done.set()

	def __del__(self):
		self.close()
