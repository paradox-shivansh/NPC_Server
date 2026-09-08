import time


class DayManager:


    def __init__(

        self,

        duration

    ):


        self.duration = duration


    def run_day(

        self,

        simulation_step

    ):


        start_time = time.time()


        while (

            time.time() - start_time

            < self.duration

        ):


            simulation_step()


            time.sleep(5)