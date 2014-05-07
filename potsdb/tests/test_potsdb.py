import potsdb
import sys
import random
import time
import os

from unittest import TestCase, main as unittest_main

try:
    HOST = os.environ['OTSDB_TEST_HOST']
except KeyError:
    sys.exit("To run tests, set environment variable OTSDB_TEST_HOST to OpenTSDB instance address (OTSDB_TEST_PORT also, but defaults to 4242)")
finally:
    PORT = int(os.environ.get('OTSDB_TEST_PORT', '4242'))

class TestPostDB(TestCase):
    def test_normal(self):
        t = potsdb.Client(HOST, port=PORT)
        for x in range(100):
            extratag = str(random.randint(0, 1000000))
            t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        self.assertEquals(t.queued, 100)

    def test_slow_mps(self):
        t = potsdb.Client(HOST, port=PORT, mps=1)
        for x in xrange(10):
            extratag = str(random.randint(0, 1000000))
            t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        self.assertEquals(t.queued, 10)

    def test_duplicate_metric(self):
        t = potsdb.Client(HOST, port=PORT)
        for x in range(10):
            t.log('test.metric2', 1, cheese='blue')
        t.wait()
        assert t.queued == 1  # should not queue duplicates

    def test_invalid_metric_name(self):
        # Attempts to send a metric with invalid name (spaces)
        t = potsdb.Client(HOST, port=PORT)
        self.assertRaises(AssertionError, lambda: t.log('test.metric2 roflcopter!', 1, cheese='blue'))
        self.assertEquals(t.queued, 0)
        t.stop()

    def test_setting_timestamp_multiple(self):
        # sends many metrics while specifying the timestamp
        t = potsdb.Client(HOST, PORT)
        ts = int(time.time())
        for x in range(100):
            t.log('test.metric4', 20, tag1='timestamptest', timestamp=ts)
            ts -= 1
        self.assertEquals(t.queued, 100)
        t.wait()

    def test_qsize_change(self, size=100):
        t = potsdb.Client(HOST, port=PORT, qsize=size)
        for x in range(5 * size):
            extratag = str(random.randint(0, 1000000))
            t.log('test.metric2', random.randint(0, 200), cheese='blue', random=extratag)
        t.wait()
        print "qsize was %s, sent %s" % (size, t.queued)
        self.assertGreaterEqual(t.queued, size)


    @classmethod
    def tearDownClass(cls):
        print 'done'


if __name__ == '__main__':
    unittest_main()
