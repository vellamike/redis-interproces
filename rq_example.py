"""
RQ seems pretty nice, especially as you can have multiple queues with different priorities.

This is a minimal working example.

You will need to start an rqworker and redis-server for this to run
"""

from redis import Redis
from rq import Queue
from my_module import add_3
import time

q = Queue(connection=Redis())
job = q.enqueue(add_3, 9)
time.sleep(1)
print job.result
