from fastapi import FastAPI
from api.router import router

app = FastAPI(
    title="Credit Scoring API",
    description="API to predict the risk of default of clients (repay, default) using a stacked ensemble model.",
    version="1.0.0"
)

# Include the modular router
app.include_router(router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the Credit Scoring API 💳"}


