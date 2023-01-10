from fastapi import FastAPI
from routers import exports

app = FastAPI(
    debug=True,
    title="CosmoRemit Microservices",
    docs_url="/docs",
    redoc_url="/",
    version="0.1.0",
    description="CosmoRemit micro service api documentations",
)

# include the exports router
app.include_router(exports.router)
