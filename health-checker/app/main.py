import time
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import make_asgi_app, Counter, Gauge, Histogram
import threading
import random
import os
import requests


version = os.getenv("VERSION", "v3.0.0")
health = 200

app = FastAPI()

# ***** Prometheus metrics *****
EIGEN_FEES_EARNED_TOTAL = Counter(
    'eigen_fees_earned_total',
    'The amount of fees earned in <unit> of underlying <token> in the <strategy> contract.',
    labelnames=["token", "unit", "strategy"]
)
EIGEN_SLASHING_STATUS = Gauge(
    'eigen_slashing_status',
    'Slashing status of the node. 1 if the node is being slashed, 0 otherwise.',
    labelnames=["avs"]
)
EIGEN_REGISTERED_STAKES = Gauge(
    'eigen_registered_stakes',
    'Operator stakes defined by the AVS in <unit> of underlying <token> in the <strategy> contract.',
    labelnames=["token", "unit", "strategy"]
)
EIGEN_PERFORMANCE_SCORE = Gauge(
    'eigen_performance_score',
    'The performance metric is a score between 0 and 100 and each developer can define their own way of calculating the score. The score is calculated based on the performance of the Node and the performance of the backing services.'
)
EIGEN_RPC_REQUEST_DURATION_SECONDS = Histogram(
    'eigen_rpc_request_duration_seconds',
    'Duration of json-rpc <method> in seconds',
    labelnames=["method", "client_version"]
)
EIGEN_RPC_REQUEST_TOTAL = Counter(
    'eigen_rpc_request_total',
    'Total of json-rpc <method> requests',
    labelnames=["method", "client_version"]
)

app.mount("/metrics", make_asgi_app())
# ***** Prometheus metrics *****


@app.get("/check/{avs_target}")
def get_option(avs_target: str):
    # Make request to AVS health check endpoint
    # If AVS is up, return 200
    # If AVS is down, raise 503
    # If AVS is up but not ready, return 206
    resp = requests.get(f"http://{avs_target}/eigen/node/health")
    return Response(content=resp.content, status_code=resp.status_code)

@app.post("/health/{status_code}")
def update_health(status_code: int):
    global health
    if status_code not in [200, 206, 503]:
        raise HTTPException(status_code=400, detail="Invalid status code")
    health = status_code


@app.get("/eigen/node/spec-version")
def get_spec_version():
    return {"api_version": "v1.0.0"}


@app.get("/eigen/node/version")
def get_version():
    return {"version": version}


@app.get("/eigen/node/health", status_code=200)
def get_health(response: Response):
    response.status_code = health


@app.get("/eigen/node/services")
def get_services():
    return {"services": [
        {
            "id": "db-1",
            "name": "Database",
            "description": "Database description",
            "status": "Up",
        },
        {
            "id": "idx-2",
            "name": "Indexer",
            "description": "Indexer description",
            "status": "Down",
        }
    ]}


@app.get("/eigen/node/services/{service_id}/health")
def get_service_health(service_id: str, response: Response):
    if service_id == "db-1":
        response.status_code = 200
    elif service_id == "idx-2":
        response.status_code = 503
    else:
        raise HTTPException(status_code=404, detail="Service not found")


class BackgroundTasks(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.eth_stakes = 32
        self.egn_stakes = 50

    def run(self) -> None:
        while True:
            earned_eth = random.random()
            self.eth_stakes += earned_eth
            earned_egn = random.random()
            self.egn_stakes += earned_egn
            slashing = 0 if random.random() < 0.6 else 1

            EIGEN_FEES_EARNED_TOTAL.labels(
                token="ETH",
                unit="ether",
                strategy="mock-avs-eth-strategy"
            ).inc(earned_eth)
            EIGEN_FEES_EARNED_TOTAL.labels(
                token="EGN",
                unit="eigen",
                strategy="mock-avs-egn-strategy"
            ).inc(earned_egn)
            EIGEN_SLASHING_STATUS.labels(
                avs="mock-avs-option-returner",
            ).set(slashing)
            EIGEN_REGISTERED_STAKES.labels(
                token="ETH",
                unit="ether",
                strategy="mock-avs-eth-strategy"
            ).set(self.eth_stakes)
            EIGEN_REGISTERED_STAKES.labels(
                token="EGN",
                unit="eigen",
                strategy="mock-avs-egn-strategy"
            ).set(self.egn_stakes)
            EIGEN_PERFORMANCE_SCORE.set(random.randint(80, 100))
            EIGEN_RPC_REQUEST_DURATION_SECONDS.labels(
                method="eth_getBlockByNumber",
                client_version="nethermind/1.19.0"
            ).observe(random.random()*0.3)
            EIGEN_RPC_REQUEST_TOTAL.labels(
                method="eth_getBlockByNumber",
                client_version="nethermind/1.19.0" 
            ).inc(1)
            EIGEN_RPC_REQUEST_DURATION_SECONDS.labels(
                method="eth_getBalance",
                client_version="nethermind/1.19.0"
            ).observe(random.random()*0.5)
            EIGEN_RPC_REQUEST_TOTAL.labels(
                method="eth_getBalance",
                client_version="nethermind/1.19.0"
            ).inc(1)
            time.sleep(5)


@app.on_event("startup")
async def startup_event():
    t = BackgroundTasks()
    t.start()
