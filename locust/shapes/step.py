from locust import LoadTestShape


class StepShape(LoadTestShape):
    stages = [
        {"duration": 30,  "users": 10,  "spawn_rate": 2},
        {"duration": 30,  "users": 30,  "spawn_rate": 5},
        {"duration": 30,  "users": 60,  "spawn_rate": 10},
        {"duration": 30,  "users": 100, "spawn_rate": 15},
        {"duration": 30,  "users": 150, "spawn_rate": 20},
    ]

    def tick(self):
        run_time = self.get_run_time()
        total = 0
        for stage in self.stages:
            total += stage["duration"]
            if run_time < total:
                return stage["users"], stage["spawn_rate"]
        return None
