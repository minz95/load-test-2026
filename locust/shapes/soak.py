from locust import LoadTestShape


class SoakShape(LoadTestShape):
    stages = [
        {"duration": 30,   "users": 50, "spawn_rate": 5},
        {"duration": 270,  "users": 50, "spawn_rate": 5},
    ]

    def tick(self):
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return stage["users"], stage["spawn_rate"]
        return None
