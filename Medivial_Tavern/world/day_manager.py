import time


class DayManager:

    def __init__(self, duration, simulation_step):

        self.duration = duration
        self.simulation_step = simulation_step

    def run_day(self, simulation_function):

        start_time = time.time()

        while time.time() - start_time < self.duration:

            simulation_function()

            time.sleep(self.simulation_step)