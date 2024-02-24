from robot_io import io

class Timer:
    def __init__(self):
        self.start_time = 0.0
        self.started = False

    def reset(self):
        self.started = False

    def start(self):
        self.start_time = io.time()
        self.started = True

    def has_elapsed(self, duration: float) -> bool:
        return self.started and (io.time() 
                                 >= self.start_time + duration)
    
    def is_started(self) -> bool:
        return self.started