import time
import numpy as np

class Timer:

    def __init__(self, precision=3):
        self.total_time = 0
        self.total_calls = 0
        self.tic_time = 0
        self.precision = precision

    def now(self):
        return int(time.process_time() * np.power(10,self.precision))

    def tic(self):
        self.tic_time = self.now()

    def toc(self):
        self.total_time += self.now() - self.tic_time
        self.total_calls += 1

    def getElapsedTime(self):
        return self.total_time

    def stats(self):
        print(f"Total time: {self.total_time/1000} s")
        print(f"Total calls: {self.total_calls}")
        print(f"Average time: {((self.total_time/np.power(10, self.precision)) / self.total_calls)} s\n")

timer_predict = Timer()
timer_outlook = Timer()
timer_outlook_global = Timer()
timer_total = Timer()
timer_fit = Timer()
timer_collisions = Timer()
