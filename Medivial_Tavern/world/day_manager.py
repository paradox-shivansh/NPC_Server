import time


class DayManager:

    def __init__(
        self,
        duration,
        simulation_step
    ):

        self.duration = duration
        self.simulation_step = simulation_step


    def run_day(
        self,
        simulation_function,
        world
    ):

        print(
            f"\n🌅 DAY {world.day_number} BEGINS"
        )

        print(
            f"Weather: {world.weather}"
        )

        print(
            f"Event: {world.tavern_event}"
        )

        print(
            f"Special Event: {world.special_event}"
        )

        start_time = time.time()

        while (
            time.time() - start_time
            < self.duration
        ):

            simulation_function(
                world
            )

            time.sleep(
                self.simulation_step
            )

        print(
            f"\n🌙 DAY {world.day_number} ENDS"
        )