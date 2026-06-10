"""
Zero-dependency API client for Korea Analysis System.
Simple `requests` wrapper — no auth, no session state needed in V0.1.
"""
from typing import Any, Optional
import requests as _requests

API_BASE_URL = "http://localhost:8000"


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
