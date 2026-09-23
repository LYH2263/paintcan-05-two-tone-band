from pydantic import BaseModel

class BandRequest(BaseModel):
    enabled: bool = False
    waist_height: float | None = None
    lower_coverage: float | None = None
    upper_coverage: float | None = None
    lower_coats: int | None = None
    upper_coats: int | None = None

class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    persist: bool = True
    band: BandRequest | None = None
