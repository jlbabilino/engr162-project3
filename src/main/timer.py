from robot_io import io

class Timer:
    """
    A helper class that acts like a stopwatch. It can be started, stopped, and
    reset. It can also check if a certain amount of time has elapsed since it
    was started.
    """
    def __init__(self):
        self.start_time = 0.0
        self.started = False

    def reset(self):
        """
        Resets timer
        """
        self.started = False

    def start(self):
        """
        Starts the timer from 0
        """
        self.start_time = io.time()
        self.started = True

    def elapsed_time(self) -> float:
        """
        Returns the time elapsed since the timer was started, or 0 if it hasn't
        """
        if self.started:
            return io.time() - self.start_time
        else:
            return 0.0

    def has_elapsed(self, duration: float) -> bool:
        """
        Returns whether the timer has been started and has elapsed the given
        duration
        """
        return self.started and (io.time() 
                                 >= self.start_time + duration)

    def is_started(self) -> bool:
        """
        Returns whether the timer has been started
        """
        return self.started
