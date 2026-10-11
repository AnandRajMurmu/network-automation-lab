from fastapi import FastAPI

app = FastAPI(
    title="Network Automation Lab API",
    description="Backend API for the network automation platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Network Automation Lab API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
