## load-test-2026

repo for load test with locust

### 1. 로컬 Python 환경에서 실행 (선택)

```bash
cd load-test-2026
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- FastAPI 앱 실행:

```bash
uvicorn app.main:app --reload --port 8000
```

- Locust로 로컬 부하 테스트:

```bash
locust -f locust/locust.py --host=http://localhost:8000
```

### 2. Kubernetes에서 mock-api + Locust Job 실행

1) Docker 이미지 빌드 (OrbStack 기준, 로컬 Docker 사용):

```bash
cd load-test-2026

# mock-api
docker build -t mock-api:latest -f app/Dockerfile .

# locust
docker build -t locust:latest -f locust/Dockerfile.locust .
```

2) Kubernetes 리소스 배포:

```bash
kubectl create ns load-test || true

kubectl apply -f manifest/mock-api-deployment.yaml -n load-test
kubectl apply -f manifest/mock-api-service.yaml -n load-test
kubectl apply -f manifest/mock-api-hpa.yaml -n load-test

kubectl apply -f manifest/locust-job.yaml -n load-test
```

3) Locust Job 로그 확인:

```bash
kubectl logs job/locust-loadtest -n load-test
```

### 3. kubectl run 으로 Spike Test 실행 (단발성 Pod)

로컬 Docker 이미지를 그대로 사용하기 위해 `image-pull-policy` 를 지정합니다.

```bash
docker build -t locust:local -f locust/Dockerfile.locust .

kubectl run spike-test \
  -n load-test \
  --image=locust:local \
  --image-pull-policy=IfNotPresent \
  --port=8089 \
  --env=TEST_TYPE=spike \
  --env=BASE_RPS=2 \
  --env=SPIKE_RPS=20 \
  --env=SPIKE_TIME=60
```

Locust 웹 UI 를 보려면:

```bash
kubectl port-forward pod/spike-test 8089:8089 -n load-test
```

브라우저에서 `http://localhost:8089` 접속.

### 4. Docker 로 Airflow + DAG 실행

Airflow + Locust 가 포함된 이미지를 빌드하고, `load_test_dag.py` 를 DAG 로 등록해서 실험을 실행합니다.

1) Airflow 이미지 빌드 및 컨테이너 실행:

```bash
cd load-test-2026
docker compose -f docker-compose.airflow.yaml up --build
```

2) Airflow UI 접속:

- 주소: `http://localhost:8080`
- 기본 계정: `admin` / `admin`

3) DAG 실행:

- DAG 리스트에서 `locust_load_test` 를 찾습니다.
- 우측에서 ▶(Trigger) 버튼을 눌러 실행합니다.

이 DAG는 컨테이너 내부에서 다음과 유사한 명령으로 Locust 부하 테스트를 실행합니다.

```bash
locust -f locust/locust.py \
  --headless \
  -u 50 \
  -r 5 \
  --run-time 60s \
  --host http://api-service
```

