from locust import HttpUser, task, between, tag, LoadTestShape
import random
import time


class ApiUser(HttpUser):
    """
    공통 API User 클래스
    - 어떤 API를 때릴지 정의
    - Load / Spike 실험은 tag와 LoadShape로 구분
    """
    wait_time = between(0.5, 1.5)

    @tag("load")
    @task(3)
    def normal_load_test(self):
        """
        Load Test용 API 호출
        안정적인 트래픽 상황 가정
        """
        with self.client.get("/api/data", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Load Test failed: {response.status_code}")

    @tag("spike")
    @task(3)
    def spike_test(self):
        """
        Spike Test용 API 호출
        갑작스러운 트래픽 폭증 상황 가정
        """
        with self.client.get("/api/data", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Spike Test failed: {response.status_code}")

    @tag("error")
    @task(1)
    def error_endpoint(self):
        """
        에러 발생 엔드포인트 테스트
        error rate 관측용
        """
        with self.client.get("/api/error", catch_response=True) as response:
            if response.status_code != 200:
                response.failure("Intentional error endpoint")

    @tag("limited")
    @task(2)
    def rate_limited_endpoint(self):
        """
        Rate Limit 테스트 엔드포인트
        429 발생 여부 관측
        """
        with self.client.get("/api/limited", catch_response=True) as response:
            if response.status_code == 429:
                response.failure("Rate limit exceeded")


# ==============================
# Spike Test 패턴 정의 (LoadShape)
# ==============================

class NormalToSpikeShape(LoadTestShape):
    """
    일정한 부하 -> 갑자기 spike -> 회복하는 Spike Test 패턴

    Stage 1: 정상 트래픽
    Stage 2: 갑자기 spike
    Stage 3: 회복
    """

    stages = [
        {"duration": 30, "users": 20, "spawn_rate": 5},     # 정상 상태 (30초)
        {"duration": 10, "users": 200, "spawn_rate": 200}, # Spike (10초)
        {"duration": 30, "users": 20, "spawn_rate": 10},   # 회복 (30초)
    ]

    def tick(self):
        """
        Locust가 매초 호출해서
        현재 users / spawn_rate를 결정
        """
        run_time = self.get_run_time()

        total_time = 0
        for stage in self.stages:
            total_time += stage["duration"]
            if run_time < total_time:
                return stage["users"], stage["spawn_rate"]

        return None 
