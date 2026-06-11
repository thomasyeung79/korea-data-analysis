import json

from ..schemas import AIReportRequest, AIReportResponse


class OpenAIReportProvider:
    provider_name = "openai"

    def __init__(self, api_key: str):
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key, timeout=4.0, max_retries=0)

    def generate(self, request: AIReportRequest) -> AIReportResponse:
        prompt = f"""
Generate a structured Korea perception report.
Return valid JSON only. No markdown.

Required JSON keys:
provider, profile_label, perception_summary, strongest_associations,
concerns_or_gaps, korea_baseline_comparison, community_average_comparison,
interpretation_profile, suggested_next_question

Use provider value "openai".

Input:
{request.model_dump_json()}
"""
        try:
            response = self.client.responses.create(
                model="gpt-4o-mini",
                input=prompt,
            )
            text = response.output_text.strip()
            data = json.loads(text)
            data["provider"] = self.provider_name
            return AIReportResponse(**data)
        except Exception as exc:
            raise RuntimeError(f"OpenAI report generation failed: {exc}") from exc
