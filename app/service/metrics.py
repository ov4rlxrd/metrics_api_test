from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.reprository.metrics import MetricsRepository
from app.schemas.device import DeviceMetricsResponse, DeviceMetricsAnalysisResponse, MetricStats


class MetricsService:
    @classmethod
    async def add_metrics_service(cls, device_id: str, x: float, y: float, z: float, session):
        new_metric = await MetricsRepository.add_metrics_repository(device_id, x, y, z, session)
        return DeviceMetricsResponse(id = new_metric.id,device_id=new_metric.device_id, x=new_metric.x, y=new_metric.y, z=new_metric.z, created_at=new_metric.created_at)

    @classmethod
    async def analyze_metrics_service(
        cls,
        device_id: str,
        session: AsyncSession,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):
        result = await MetricsRepository.analyze_metrics_repository(device_id, session, date_from, date_to)

        return DeviceMetricsAnalysisResponse(
            device_id=device_id,
            x=MetricStats(
                min=result["x_min"],
                max=result["x_max"],
                count=result["x_count"],
                sum=result["x_sum"],
                median=result["x_median"],
            ),
            y=MetricStats(
                min=result["y_min"],
                max=result["y_max"],
                count=result["y_count"],
                sum=result["y_sum"],
                median=result["y_median"],
            ),
            z=MetricStats(
                min=result["z_min"],
                max=result["z_max"],
                count=result["z_count"],
                sum=result["z_sum"],
                median=result["z_median"],
            ),
        )