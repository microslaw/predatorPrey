import time

class Timer:
    @staticmethod
    def now():
        return int(time.process_time() * 1_000)

    def __init__(self):
        self.total_time = 0
        self.total_calls = 0
        self.tic_time = 0

    def tic(self):
        self.tic_time = Timer.now()

    def toc(self):
        self.total_time += Timer.now() - self.tic_time
        self.total_calls += 1

    def stats(self):
        print(f"Total time: {int(self.total_time/1000)} s")
        print(f"Total calls: {self.total_calls}")
        print(f"Average time: {int(self.total_time / self.total_calls)} ms")

timer_predict = Timer()
timer_state = Timer()
timer_total = Timer()
