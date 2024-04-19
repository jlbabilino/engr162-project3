from typing import Callable

class LambdaCommand:
    """
    Command to run a non-blocking lambda function instantly
    """
    def __init__(self, lambda_to_run: Callable[[], None]):
        self.lambda_to_run = lambda_to_run

    def initialize(self):
        self.lambda_to_run()

    def execute(self) -> bool:
        return True
