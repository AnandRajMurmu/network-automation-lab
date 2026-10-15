from api.routes.devices import router as devices_router
from api.routes.health import router as health_router
from api.routes.templates import router as templates_router
from fastapi import FastAPI

app = FastAPI(
    title="Network Automation Lab API",
    description="Backend API for the network automation platform",
    version="0.1.0",
    root_path="/api",
)

app.include_router(health_router)
app.include_router(devices_router)
app.include_router(templates_router)
