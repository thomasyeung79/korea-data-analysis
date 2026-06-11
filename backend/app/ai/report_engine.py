from ..config import settings
from ..schemas import AIReportRequest, AIReportResponse
from .local_provider import LocalReportProvider
from .openai_provider import OpenAIReportProvider


class AIReportEngine:
    def __init__(self):
        self.local_provider = LocalReportProvider()

    def generate(self, request: AIReportRequest) -> AIReportResponse:
        if settings.OPENAI_API_KEY:
            try:
                return OpenAIReportProvider(settings.OPENAI_API_KEY).generate(request)
            except Exception:
                pass
        return self.local_provider.generate(request)
