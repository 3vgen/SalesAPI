from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from app.routers.sales import router as sales_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="Сервис анализа дневных продаж ресторана",
    version=settings.APP_VERSION,
)

app.include_router(sales_router, prefix="/api/v1")


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = "; ".join(
        f"{' -> '.join(str(l) for l in e['loc'])}: {e['msg']}" for e in exc.errors()
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "Sales Analyzer is running"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)