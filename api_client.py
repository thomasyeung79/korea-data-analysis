"""
Zero-dependency API client for Korea Analysis System.
Simple `requests` wrapper — no auth, no session state needed in V0.1.
"""
from typing import Any, Optional
import os
import requests as _requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class APIClient:
    """Minimal API client. Stateless — no auth for V0.1."""

    def _request(self, method: str, path: str, **kwargs) -> Any:
        url = f"{API_BASE_URL}{path}"
        try:
            resp = _requests.request(
                method, url, timeout=10,
                headers={"Content-Type": "application/json"},
                **kwargs,
            )
        except _requests.ConnectionError:
            raise ConnectionError(
                f"Cannot connect to {API_BASE_URL}. "
                "Make sure the backend is running."
            )

        if resp.status_code >= 400:
            detail = resp.text
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                pass
            raise Exception(detail)

        if resp.status_code == 204:
            return None
        return resp.json()

    # ── Health ──

    def health(self) -> dict:
        return self._request("GET", "/api/v1/health")

    # ── Country scores ──

    def get_country_scores(
        self,
        country: Optional[str] = None,
        year: Optional[int] = None,
        category: Optional[str] = None,
    ) -> list[dict]:
        params = {}
        if country:
            params["country"] = country
        if year:
            params["year"] = year
        if category:
            params["category"] = category
        return self._request("GET", "/api/v1/countries", params=params)

    def get_country(self, country: str) -> list[dict]:
        return self._request("GET", f"/api/v1/countries/{country}")

    def create_country_score(
        self,
        country: str,
        year: int,
        category: str,
        score: float,
        source: Optional[str] = None,
    ) -> dict:
        return self._request(
            "POST",
            "/api/v1/countries",
            json={
                "country": country,
                "year": year,
                "category": category,
                "score": score,
                "source": source,
            },
        )

    def list_categories(self) -> list[str]:
        return self._request("GET", "/api/v1/countries/categories/list")

    def list_countries(self) -> list[str]:
        return self._request("GET", "/api/v1/countries/countries/list")

    # ── Perception surveys ──

    def submit_survey(
        self,
        economy_score: int,
        technology_score: int,
        education_score: int,
        culture_score: int,
        global_influence_score: int,
        quality_of_life_score: int,
        display_name: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> dict:
        return self._request(
            "POST",
            "/api/v1/perception-surveys",
            json={
                "display_name": display_name or "Anonymous",
                "economy_score": economy_score,
                "technology_score": technology_score,
                "education_score": education_score,
                "culture_score": culture_score,
                "global_influence_score": global_influence_score,
                "quality_of_life_score": quality_of_life_score,
                "comment": comment,
            },
        )

    def get_surveys(self, limit: int = 20) -> list[dict]:
        return self._request("GET", "/api/v1/perception-surveys", params={"limit": limit})

    def get_survey_stats(self) -> dict:
        return self._request("GET", "/api/v1/perception-surveys/stats")

    def get_community_summary(self) -> dict:
        return self._request("GET", "/api/v1/perception-surveys/community-summary")

    # ── AI reports ──

    def generate_perception_report(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/ai/perception-report", json=payload)
