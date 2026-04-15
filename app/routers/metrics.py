from datetime import datetime

from starlette import status

from app.database import SessionDep
from fastapi import APIRouter
from app.schemas.device import DeviceMetricsAdd, DeviceMetricsResponse, DeviceMetricsAnalysisResponse
from app.service.metrics import MetricsService
metrics_router = APIRouter(prefix="/metrics", tags=["Metrics"])


@metrics_router.post("", status_code=status.HTTP_201_CREATED)
async def add_metrics(metrics: DeviceMetricsAdd, session: SessionDep) -> DeviceMetricsResponse:
    return await MetricsService.add_metrics_service(metrics.device_id, metrics.x,metrics.y,metrics.z, session)


@metrics_router.get("/{device_id}/analytics", status_code=status.HTTP_200_OK)
async def get_metrics_analytics(
    device_id: str,
    session: SessionDep,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> DeviceMetricsAnalysisResponse:
    return await MetricsService.analyze_metrics_service(device_id, session, date_from, date_to)
