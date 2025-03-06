from fastapi import FastAPI
import logging
from prometheus_client import Counter

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
