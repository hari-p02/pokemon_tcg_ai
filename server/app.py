from fastapi import FastAPI
from pktcgai.routes.endpoints import router as pktcgai_router
import uvicorn

app = FastAPI()

app.include_router(pktcgai_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)