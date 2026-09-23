from pydantic import BaseModel


class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    persist: bool = True
    # 墙腰双色分带
    band: bool = False
    waist_height: float | None = None
    lower_coverage: float | None = None
    lower_coats: int | None = None
    upper_coverage: float | None = None
    upper_coats: int | None = None
