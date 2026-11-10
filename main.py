from app.routes.users import router as users_router
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from app.operations import add, subtract, multiply, divide
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="FastAPI Calculator",
    description="A calculator application using FastAPI",
    version="1.0.0"
)

# Configure HTML templates
templates = Jinja2Templates(directory="templates")

# Register user management routes
app.include_router(users_router)


# Request model
class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator("a", "b")
    @classmethod
    def validate_numbers(cls, value):
        return value


# Successful response model
class OperationResponse(BaseModel):
    result: float


# Error response model
class ErrorResponse(BaseModel):
    error: str


# Handle HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(
        "HTTPException on %s: %s",
        request.url.path,
        exc.detail
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


# Handle invalid request data
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    error_messages = "; ".join(
        f"{error['loc'][-1]}: {error['msg']}"
        for error in exc.errors()
    )

    logger.error(
        "Validation error on %s: %s",
        request.url.path,
        error_messages
    )

    return JSONResponse(
        status_code=400,
        content={"error": error_messages}
    )


# Health check endpoint for Docker
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# Addition endpoint
@app.post(
    "/add",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def add_route(operation: OperationRequest):
    try:
        result = add(operation.a, operation.b)
        return OperationResponse(result=result)

    except Exception as error:
        logger.error("Addition error: %s", error)
        raise HTTPException(status_code=400, detail=str(error))


# Subtraction endpoint
@app.post(
    "/subtract",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def subtract_route(operation: OperationRequest):
    try:
        result = subtract(operation.a, operation.b)
        return OperationResponse(result=result)

    except Exception as error:
        logger.error("Subtraction error: %s", error)
        raise HTTPException(status_code=400, detail=str(error))


# Multiplication endpoint
@app.post(
    "/multiply",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def multiply_route(operation: OperationRequest):
    try:
        result = multiply(operation.a, operation.b)
        return OperationResponse(result=result)

    except Exception as error:
        logger.error("Multiplication error: %s", error)
        raise HTTPException(status_code=400, detail=str(error))


# Division endpoint
@app.post(
    "/divide",
    response_model=OperationResponse,
    responses={400: {"model": ErrorResponse}}
)
async def divide_route(operation: OperationRequest):
    try:
        result = divide(operation.a, operation.b)
        return OperationResponse(result=result)

    except ValueError as error:
        logger.error("Division error: %s", error)
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        logger.exception("Unexpected division error")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


# Run application directly
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
