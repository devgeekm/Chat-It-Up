from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router( chat_router.router, prefix='/chat', tags=['Chat'] )
# ==> Route for blob storage
# ==> Route for other azure resources ...