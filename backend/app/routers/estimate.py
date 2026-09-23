from fastapi import APIRouter, HTTPException
from app.schemas.estimate import EstimateRequest
from app.services.paint_service import PaintService

router = APIRouter()


@router.post("/estimate")
def post_estimate(body: EstimateRequest):
    with PaintService() as s:
        try:
            r = s.estimate(
                body.room_id, body.persist, body.coats, body.coverage,
                band=body.band, waist_height=body.waist_height,
                lower_coverage=body.lower_coverage, lower_coats=body.lower_coats,
                upper_coverage=body.upper_coverage, upper_coats=body.upper_coats,
            )
        except ValueError as e:
            # 腰线越界 / 涂布率或遍数非正：整单拒绝，不写记录
            raise HTTPException(status_code=400, detail=str(e))
        if not r: raise HTTPException(404)
        return r
