import csv
import io

from backend.models.schemas import AnalysisReport


class ReportService:
    def to_csv(self, report: AnalysisReport) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["metric", "score"])
        writer.writerow(["overall", report.overall_similarity])
        for key, value in report.breakdown.model_dump().items():
            writer.writerow([key, value])
        return output.getvalue()

