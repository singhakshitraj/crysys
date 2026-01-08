from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_zones: int
    active_disasters: int
    critical_zones: int
    pending_sos_requests: int
