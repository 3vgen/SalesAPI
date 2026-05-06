import logging

from app.core.config import settings
from app.schemas.sale import DishResult, SaleItem, SalesResponse

logger = logging.getLogger(__name__)


class SalesAnalysisService:
    def __init__(
        self,
        low_margin_threshold: float = settings.LOW_MARGIN_THRESHOLD,
        top_count: int = settings.TOP_DISHES_COUNT,
    ) -> None:
        self._threshold = low_margin_threshold
        self._top_count = top_count

    def analyze(self, sales: list[SaleItem]) -> SalesResponse:
        logger.info("Анализ %d позиций", len(sales))
        
        # Сортируем блюда по убыванию маржинальности и берем топ-N
        top_margin = sorted(sales, key=lambda s: s.margin_percent, reverse=True)[: self._top_count]
        
        # Отбираем блюда с маржинальностью ниже заданного порога (убыточные)
        loss_making = [s for s in sales if s.margin_percent < self._threshold]

        return SalesResponse(
            top_margin_dishes=[self._to_result(s) for s in top_margin],
            loss_making=[self._to_result(s) for s in loss_making],
            total_revenue=round(sum(s.revenue for s in sales), 2),
            total_margin=round(sum(s.profit for s in sales), 2),
            suggestions=self._suggestions(sales, loss_making),
        )

    def _to_result(self, item: SaleItem) -> DishResult:
        return DishResult(
            dish=item.dish,
            margin_percent=item.margin_percent,
            revenue=item.revenue,
            profit=item.profit,
        )

    def _suggestions(self, sales: list[SaleItem], loss_making: list[SaleItem]) -> list[str]:
        tips: list[str] = []

        for item in loss_making:
            tips.append(
                f"Увеличить цену на «{item.dish}» — маржа {item.margin_percent}% ниже порога {self._threshold}%"
            )

        top_revenue = max(sales, key=lambda s: s.revenue)
        tips.append(f"«{top_revenue.dish}» даёт максимальную выручку — добавить в рекомендации")

        top_margin = max(sales, key=lambda s: s.margin_percent)
        if top_margin.dish != top_revenue.dish:
            tips.append(
                f"«{top_margin.dish}» — наивысшая маржа ({top_margin.margin_percent}%), стоит продвигать"
            )

        avg_qty = sum(s.quantity for s in sales) / len(sales)
        for item in sales:
            if item.quantity < avg_qty * 0.5:
                tips.append(f"«{item.dish}» продаётся мало ({item.quantity} шт.) — проверить спрос")

        return tips
