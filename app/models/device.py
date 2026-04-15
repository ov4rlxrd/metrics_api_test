from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Model

class DeviceMetrics(Model):
    __tablename__ = 'devices_metrics'

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column()
    x: Mapped[float] = mapped_column()
    y: Mapped[float] = mapped_column()
    z: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(), nullable=False)

