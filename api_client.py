"""
Zero-dependency API client for Korea Analysis System.
Simple `requests` wrapper — no auth, no session state needed in V0.1.
"""
from typing import Any, Optional
import os
import requests as _requests


def _get_api_base_url() -> str:
    if os.getenv("API_BASE_URL"):
        return os.environ["API_BASE_URL"]
    try:
        import streamlit as st

        return str(st.secrets.get("API_BASE_URL", "http://localhost:8000"))
    except Exception:
        return "http://localhost:8000"


API_BASE_URL = _get_api_base_url()

BACKEND_UNAVAILABLE_MESSAGE = """Backend API is not available.

For local development, start the FastAPI backend first:

cd backend
uvicorn app.main:app --reload --port 8000

Then restart the Streamlit frontend:

streamlit run app.py

For cloud deployment, deploy the FastAPI backend separately and set API_BASE_URL in Streamlit Secrets."""


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
            return self._local_request(method, path, **kwargs)

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

    def _local_request(self, method: str, path: str, **kwargs) -> Any:
        """Run Streamlit Cloud without a separate FastAPI process."""
        payload = kwargs.get("json") or {}
        params = kwargs.get("params") or {}

        if method == "GET" and path == "/api/v1/health":
            return {
                "status": "ok",
                "version": "2.0.0",
                "service": "Korea Study & Career Decision Agent",
                "mode": "streamlit-local",
            }

        if method == "POST" and path == "/api/v1/study-cost/calculate":
            from backend.app.services.study_cost_config import calculate_costs, generate_cost_explanation

            city = payload.get("city", "Seoul")
            school_type = payload.get("school_type", "Undergraduate")
            housing_type = payload.get("housing_type", "Shared Apartment")
            lifestyle = payload.get("lifestyle_level", "Standard")
            language = "zh" if payload.get("language") == "zh" else "en"
            result = calculate_costs(city, school_type, housing_type, lifestyle)
            return {
                "monthly_cost": result["monthly_cost"],
                "annual_cost": result["annual_cost"],
                "breakdown": result["breakdown"],
                "ai_summary": generate_cost_explanation(
                    city, school_type, housing_type, lifestyle, result, language=language
                ),
            }

        if method == "POST" and path == "/api/v1/job-market/analyze":
            from backend.app.services.job_market_config import (
                EXPERIENCE_LEVELS,
                KOREAN_LEVELS,
                ROLES,
                analyze_job_market,
                generate_preparation_plan,
            )

            language = "zh" if payload.get("language") == "zh" else "en"
            role = payload.get("role") if payload.get("role") in ROLES else "Backend Developer"
            exp = payload.get("experience_level") if payload.get("experience_level") in EXPERIENCE_LEVELS else "0-2 years"
            kl = payload.get("korean_level") if payload.get("korean_level") in KOREAN_LEVELS else "None"
            result = analyze_job_market(role, exp, kl, language=language)
            result["ai_plan"] = generate_preparation_plan(role, exp, kl, language=language)
            return result

        if method == "POST" and path == "/api/v1/decision-report/generate":
            from backend.app.services.decision_report_config import generate_decision_report

            return generate_decision_report(
                goal=payload.get("goal", "Study"),
                target_city=payload.get("target_city", "Seoul"),
                school_type=payload.get("school_type", "Not Applicable"),
                housing_type=payload.get("housing_type", "Not Applicable"),
                lifestyle_level=payload.get("lifestyle_level", "Standard"),
                target_role=payload.get("target_role", "Not Applicable"),
                experience_level=payload.get("experience_level", "0-2 years"),
                korean_level=payload.get("korean_level", "None"),
                monthly_budget=max(int(payload.get("monthly_budget", 0)), 0),
                language="zh" if payload.get("language") == "zh" else "en",
            )

        if method == "POST" and path == "/api/v1/news-policy/search":
            from backend.app.services.news_policy_config import (
                CATEGORIES,
                TIME_RANGES,
                generate_action_suggestions,
                generate_trend_summary,
                search_items,
            )

            language = "zh" if payload.get("language") == "zh" else "en"
            category = payload.get("category", "All")
            if category not in CATEGORIES and category != "All":
                category = "All"
            time_range = payload.get("time_range", "Last 30 days")
            if time_range not in TIME_RANGES:
                time_range = "Last 30 days"
            keyword = payload.get("keyword", "")
            results = search_items(keyword=keyword, category=category, time_range=time_range)
            serialisable = []
            for item in results:
                item_copy = dict(item)
                item_copy["relevance_score"] = float(item_copy.get("relevance_score", 0))
                serialisable.append(item_copy)
            return {
                "results": serialisable,
                "ai_summary": generate_trend_summary(results, keyword, language=language),
                "action_suggestions": generate_action_suggestions(results, keyword, language=language),
                "result_count": len(serialisable),
            }

        if method == "GET" and path.endswith("/history"):
            return []

        raise ConnectionError(BACKEND_UNAVAILABLE_MESSAGE)

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

    # ── Job Market Analyzer ──

    def analyze_job_market(self, role: str, experience_level: str, korean_level: str, language: str = "en") -> dict:
        return self._request(
            "POST",
            "/api/v1/job-market/analyze",
            json={
                "role": role,
                "experience_level": experience_level,
                "korean_level": korean_level,
                "language": language,
            },
        )

    def get_job_market_history(self, limit: int = 10) -> list[dict]:
        return self._request("GET", "/api/v1/job-market/history", params={"limit": limit})

    # ── News & Policy ──

    def search_news_policy(self, keyword: str = "", category: str = "All",
                           time_range: str = "Last 30 days", language: str = "en") -> dict:
        return self._request(
            "POST",
            "/api/v1/news-policy/search",
            json={
                "keyword": keyword,
                "category": category,
                "time_range": time_range,
                "language": language,
            },
        )

    def get_news_policy_history(self, limit: int = 10) -> list[dict]:
        return self._request("GET", "/api/v1/news-policy/history", params={"limit": limit})

    # ── Decision Report ──

    def generate_decision_report(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/decision-report/generate", json=payload)

    def get_decision_report_history(self, limit: int = 10) -> list[dict]:
        return self._request("GET", "/api/v1/decision-report/history", params={"limit": limit})

    # ── AI reports ──

    def generate_perception_report(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/ai/perception-report", json=payload)

    # ── Study Cost Calculator ──

    def calculate_study_cost(self, city: str, school_type: str,
                              housing_type: str, lifestyle_level: str, language: str = "en") -> dict:
        return self._request(
            "POST",
            "/api/v1/study-cost/calculate",
            json={
                "city": city,
                "school_type": school_type,
                "housing_type": housing_type,
                "lifestyle_level": lifestyle_level,
                "language": language,
            },
        )

    def get_study_cost_history(self, limit: int = 10) -> list[dict]:
        return self._request("GET", "/api/v1/study-cost/history", params={"limit": limit})
