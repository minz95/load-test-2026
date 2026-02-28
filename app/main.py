from fastapi import FastAPI, Response
import time
import random
import asyncio
from threading import Lock

app = FastAPI()

current_requests = 0
lock = Lock()

RATE_LIMIT = 50   # 동시 요청 제한


@app.middleware("http")
async def count_requests(request, call_next):
    global current_requests

    with lock:
        current_requests += 1

    start_time = time.time()
    response = await call_next(request)

    with lock:
        current_requests -= 1

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/api/data")
async def get_data():
    # 정상 API (랜덤 지연)
    delay = random.uniform(0.05, 0.3)
    await asyncio.sleep(delay)

    return {"status": "ok", "delay": delay}


@app.get("/api/error")
async def get_error():
    # 일부러 에러 발생
    if random.random() < 0.2:  # 20% 확률로 에러
        return Response(status_code=500, content="Internal Server Error")

    await asyncio.sleep(random.uniform(0.05, 0.2))
    return {"status": "ok"}


@app.get("/api/limited")
async def limited_api():
    global current_requests

    if current_requests > RATE_LIMIT:
        return Response(status_code=429, content="Too Many Requests")

    await asyncio.sleep(random.uniform(0.1, 0.4))
    return {"status": "ok", "current_requests": current_requests}
