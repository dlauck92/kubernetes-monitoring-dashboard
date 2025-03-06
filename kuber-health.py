from fastapi import FastAPI
import random
import time
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kuberhealth")

# Prometheus Metrics
REQUEST_COUNT = Counter("request_count", "Total request count", ["endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["endpoint"])

@app.get("/")
def home():
    """Basic Home Endpoint"""
    REQUEST_COUNT.labels(endpoint="home").inc()
    return {"message": "KubeHealth API is running!"}

@app.get("/health")
def health_check():
    """Health check endpoint with simulated failures"""
    REQUEST_COUNT.labels(endpoint="health").inc()
    start_time = time.time()
    
    # Simulate a failure 20% of the time
    if random.random() < 0.2:
        logger.error("Health check failed!")
        return Response(status_code=500, content="Service Unhealthy")
    
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint="health").observe(latency)
    return {"status": "healthy", "latency": latency}

@app.get("/metrics")
def metrics():
    """Exposes Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
