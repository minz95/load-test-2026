from locust import HttpUser, task, between, tag


class ApiUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @tag("load")
    @task(3)
    def normal_load_test(self):
        with self.client.get("/api/data", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Load Test failed: {response.status_code}")

    @tag("spike")
    @task(3)
    def spike_test(self):
        with self.client.get("/api/data", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Spike Test failed: {response.status_code}")

    @tag("error")
    @task(1)
    def error_endpoint(self):
        with self.client.get("/api/error", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Intentional error endpoint")

    @tag("limited")
    @task(2)
    def rate_limited_endpoint(self):
        with self.client.get("/api/limited", catch_response=True) as response:
            if response.status_code == 429:
                response.failure("Rate limit exceeded")
