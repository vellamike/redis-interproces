
"""
Create a few processes and send them information using an in-memory Redis DB for interprocess communcation.
"""

from multiprocessing import Process
from redis import Redis
import time

class PlusFiveProcessor(Process):
    """
    Processor watches its input queue, adds five to any value on it and
    adds that to its output queue
    """
    def __init__(self, input_queue, output_queue):
        super(PlusFiveProcessor, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.redis_connection = Redis()

    def worker(self, value):
        time.sleep(3) # pretend to do some work
        return int(value) + 5

    def run(self):
        while True:
            dequed = self.redis_connection.rpop(self.input_queue)
            if dequed:
                result = self.worker(dequed)
                self.redis_connection.lpush(self.output_queue, result)
            time.sleep(0.1) # keep CPU happy

class TimesTenProcessor(Process):
    """
    Processor watches its input queue, multiplies any value on it by ten
    and appends that value to its output queue
    """
    def __init__(self, input_queue, output_queue):
        super(TimesTenProcessor, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.redis_connection = Redis()

    def worker(self, value):
        time.sleep(2) # pretend to do some work
        return int(value) * 10

    def run(self):
        while True:
            dequed = self.redis_connection.rpop(self.input_queue)
            if dequed:
                result = self.worker(dequed)
                self.redis_connection.lpush(self.output_queue, result)
            time.sleep(0.1) # keep CPU happy

if __name__ == '__main__':
    print "Main loop started, processes working, you will see output in 20s"
    # Create some processes:
    times_ten_input_queue = 'times_10_input'
    times_ten_output_queue = 'times_10_output'
    plus_five_input_queue = 'plus_5_input'
    plus_five_output_queue = 'plus_5_output'
    
    times_ten = TimesTenProcessor(times_ten_input_queue,times_ten_output_queue)
    plus_five = PlusFiveProcessor(plus_five_input_queue,plus_five_output_queue)
    #kick the processes off
    times_ten.start()
    plus_five.start()
    redis_connection = Redis()
    # Feed them processes some data through their queues
    for i in range(5):
        redis_connection.lpush(times_ten_input_queue, i)
    for i in range(5):
        redis_connection.lpush(plus_five_input_queue, i)

    time.sleep(20) #wait for the processors to finish
    #let's depopulate the times 10 queue:
    num_elements = redis_connection.llen(times_ten_output_queue)
    for i in range(num_elements):
        print redis_connection.rpop(times_ten_output_queue)
