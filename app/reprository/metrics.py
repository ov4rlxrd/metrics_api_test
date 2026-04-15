from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.device import DeviceMetrics


class MetricsRepository:
    @classmethod
    async def add_metrics_repository(cls, device_id: str, x: float, y: float, z: float, session) -> DeviceMetrics:
        new_metric = DeviceMetrics(device_id=device_id, x=x, y=y, z=z)
        session.add(new_metric)
        await session.commit()
        await session.refresh(new_metric)
        return new_metric

    @classmethod
    async def analyze_metrics_repository(
        cls,
        device_id: str,
        session: AsyncSession,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):
        stmt = select(
            func.coalesce(func.min(DeviceMetrics.x), 0.0).label("x_min"),
            func.coalesce(func.max(DeviceMetrics.x), 0.0).label("x_max"),
            func.count(DeviceMetrics.x).label("x_count"),
            func.coalesce(func.sum(DeviceMetrics.x), 0.0).label("x_sum"),
            func.coalesce(func.percentile_cont(0.5).within_group(DeviceMetrics.x), 0.0).label("x_median"),
            func.coalesce(func.min(DeviceMetrics.y), 0.0).label("y_min"),
            func.coalesce(func.max(DeviceMetrics.y), 0.0).label("y_max"),
            func.count(DeviceMetrics.y).label("y_count"),
            func.coalesce(func.sum(DeviceMetrics.y), 0.0).label("y_sum"),
            func.coalesce(func.percentile_cont(0.5).within_group(DeviceMetrics.y), 0.0).label("y_median"),
            func.coalesce(func.min(DeviceMetrics.z), 0.0).label("z_min"),
            func.coalesce(func.max(DeviceMetrics.z), 0.0).label("z_max"),
            func.count(DeviceMetrics.z).label("z_count"),
            func.coalesce(func.sum(DeviceMetrics.z), 0.0).label("z_sum"),
            func.coalesce(func.percentile_cont(0.5).within_group(DeviceMetrics.z), 0.0).label("z_median"),
        ).where(DeviceMetrics.device_id == device_id)

        if date_from is not None:
            stmt = stmt.where(DeviceMetrics.created_at >= date_from)
        if date_to is not None:
            stmt = stmt.where(DeviceMetrics.created_at <= date_to)

        result = await session.execute(stmt)
        return dict(result.mappings().one())
