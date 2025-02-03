from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from router.index import router as api_router
from schemas.error_schema import ErrorResponse, _ErrorResponseData

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler("agent_interactions.log"),  # Log to a file
        # logging.StreamHandler()  # Optional: also log to console
    ]
)

logger = logging.getLogger()

# Set environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
  title="CV4Hire Backend API",
  version="1.0.0",
  description="API functionality for CV4Hire Backend",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://cv4hire.in"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API routes
app.include_router(api_router)

# add /health route
@app.get("/health")
async def health_check():
  return {"status": "ok"}


# Custom exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    error_response = ErrorResponse(
        success=False,
        data=_ErrorResponseData(message=exc.detail)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )