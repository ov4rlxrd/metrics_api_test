from pydantic import BaseModel, Field, ConfigDict, field_validator, EmailStr


class DeviceMetricsAdd(BaseModel):
    device_id: str
    x:float = Field(default=0.0)
    y:float = Field(default=0.0)
    z:float = Field(default=0.0)

class DeviceMetricsResponse(BaseModel):
    device_id: str
    x:float
    y:float
    z:float


class MetricStats(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float


class DeviceMetricsAnalysisResponse(BaseModel):
    device_id: str
    x: MetricStats
    y: MetricStats
    z: MetricStats