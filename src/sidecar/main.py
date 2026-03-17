from fastapi import FastAPI

app = FastAPI(title="CoachMate Sidecar")


@app.get("/")
async def root():
    return {"message": "CoachMate Sidecar is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
