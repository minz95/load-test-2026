from locust import LoadTestShape


class SpikeShape(LoadTestShape):
    stages = [
        {"duration": 60,  "users": 20,  "spawn_rate": 5},
        {"duration": 30,  "users": 200, "spawn_rate": 200},
        {"duration": 60,  "users": 20,  "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return stage["users"], stage["spawn_rate"]
        return None
