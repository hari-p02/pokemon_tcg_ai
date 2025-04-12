from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pktcgai.routes.endpoints import router as pktcgai_router
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pktcgai_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)