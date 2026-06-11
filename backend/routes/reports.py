from fastapi import APIRouter, Response

from backend.models.schemas import AnalysisRequest
from backend.services.analysis_service import AnalysisService
from backend.services.report_service import ReportService

router = APIRouter()
analysis_service = AnalysisService()
report_service = ReportService()


@router.post("/json")
async def report_json(payload: AnalysisRequest) -> dict:
    report = await analysis_service.compare(payload)
    return report.model_dump()


@router.post("/csv")
async def report_csv(payload: AnalysisRequest) -> Response:
    report = await analysis_service.compare(payload)
    csv_data = report_service.to_csv(report)
    return Response(csv_data, media_type="text/csv")

