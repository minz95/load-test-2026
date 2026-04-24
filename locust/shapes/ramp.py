from locust import LoadTestShape


class RampShape(LoadTestShape):
    stages = [
        {"duration": 30,  "users": 20,  "spawn_rate": 1},
        {"duration": 30,  "users": 60,  "spawn_rate": 2},
        {"duration": 60,  "users": 100, "spawn_rate": 2},
        {"duration": 30,  "users": 60,  "spawn_rate": 2},
        {"duration": 30,  "users": 20,  "spawn_rate": 2},
    ]

    def tick(self):
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return stage["users"], stage["spawn_rate"]
        return None
