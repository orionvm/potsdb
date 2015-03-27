import potsdb
import sys
import random
import time
import os
import socket

from unittest import TestCase, main as unittest_main

HOST = os.environ.get('OTSDB_TEST_HOST', '127.0.0.1')
PORT = int(os.environ.get('OTSDB_TEST_PORT', '42424'))

def _get_client(**kwargs):
  my_kwargs = { "port": PORT, "check_host": False, "test_mode": True }
  my_kwargs.update(kwargs)
  return potsdb.Client(HOST, **my_kwargs)

class TestPotsDB(TestCase):

    def test_normal(self):
        t = _get_client()
        for x in range(100):
            extratag = str(random.randint(0, 1000000))
            t.log('test.metric1', random.randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        self.assertEquals(t.queued, 100)
        self.assertFalse(t.t.is_alive())

    def test_slow_mps(self):
        t = _get_client(mps=1)
        for x in xrange(10):
            extratag = str(random.randint(0, 1000000))
            t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        self.assertEquals(t.queued, 10)

    def test_duplicate_metric(self):
        t = _get_client()
        for x in range(10):
            t.log('test.metric3', 1, cheese='blue')
        t.wait()
        assert t.queued == 1  # should not queue duplicates

    def test_invalid_metric_name(self):
        # Attempts to send a metric with invalid name (spaces)
        t = _get_client()
        self.assertRaises(AssertionError, lambda: t.log('test.metric2 roflcopter!', 1, cheese='blue'))
        self.assertEquals(t.queued, 0)
        t.stop()

    def test_setting_timestamp_multiple(self):
        # sends many metrics while specifying the timestamp
        t = _get_client()
        ts = int(time.time())
        for x in range(100):
            t.log('test.metric4', 20, tag1='timestamptest', timestamp=ts)
            ts -= 1
        self.assertEquals(t.queued, 100)
        t.wait()

    def test_qsize_change(self, size=100):
        t = _get_client(qsize=size)
        for x in range(5 * size):
            extratag = str(random.randint(0, 1000000))
            t.log('test.metric5', random.randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        print "qsize was %s, sent %s" % (size, t.queued)
        self.assertGreaterEqual(t.queued, size)

    def test_timeout_from_check_host(self):
        self.assertRaises(socket.error, lambda: _get_client(check_host=True))

    def test_timeout_no_checkhost(self):
        t = _get_client()
        t.log('test.metric6', 100)
        self.assertEquals(t.queued, 1)
        self.assertTrue(t.t.is_alive())
        t.stop()

    def test_protocol_integer(self):
        t = _get_client(host_tag='tester')
        output = t.log('test.metric7', 100, timestamp='1234567890')
        self.assertEquals(output, "put test.metric7 1234567890 100 host=tester\n")

    def test_protocol_float(self):
        t = _get_client(host_tag='tester')
        output = t.log('test.metric8', 0.48569, timestamp='1234567890')
        self.assertEquals(output, "put test.metric8 1234567890 0.48569 host=tester\n")

    def test_automatic_timestamp(self):
        t = _get_client()
        output = t.log('test.metric9', 123)
        timestamp = int(output.split(' ')[2])
        self.assertTrue( time.time() - timestamp < 1) # within 1 seconds of current time

    @classmethod
    def tearDownClass(cls):
        print 'done'


if __name__ == '__main__':
    unittest_main()
