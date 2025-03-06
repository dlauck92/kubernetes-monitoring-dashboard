from fastapi import FastAPI
import logging
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kuberhealth")

# Prometheus Metrics
REQUEST_COUNT = Counter("request_count", "Total request count", ["endpoint"])

@app.get("/")
def home():
    """Basic Home Endpoint"""
    REQUEST_COUNT.labels(endpoint="home").inc()
    return {"message": "KubeHealth API is running!"}

@app.get("/metrics")
def metrics():
    """Exposes Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
