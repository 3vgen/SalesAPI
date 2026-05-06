import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.sale import SalesRequest, SalesResponse
from app.services.sales_analysis import SalesAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sales", tags=["Sales"])


def get_service() -> SalesAnalysisService:
    """

    (Dependency Injection).

    Создает экземпляр сервиса анализа продаж.

    Вынесено в отдельную функцию, чтобы:

    - можно было легко подменить сервис в тестах (dependency_overrides)

    - не привязывать endpoint к конкретной реализации

    """
    return SalesAnalysisService()


@router.post("/analyze_sales", response_model=SalesResponse)
async def analyze_sales(
    request: SalesRequest,
    # Получаем сервис через механизм зависимостей FastAPI
    service: SalesAnalysisService = Depends(get_service),
) -> SalesResponse:
    try:
        return service.analyze(request.sales)
    except Exception as exc:
        logger.exception("Ошибка анализа: %s", exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка")
