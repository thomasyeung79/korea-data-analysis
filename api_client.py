"""
Zero-dependency API client for Korea Compass.
Simple `requests` wrapper with local fallback for Streamlit-only demos.
"""
from typing import Any, Optional
import os
import requests as _requests


def _get_api_base_url() -> Optional[str]:
    if os.getenv("API_BASE_URL"):
        return os.environ["API_BASE_URL"]
    try:
        import streamlit as st

        configured_url = st.secrets.get("API_BASE_URL")
        return str(configured_url) if configured_url else None
    except Exception:
        return None


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
        if not API_BASE_URL:
            return self._local_request(method, path, **kwargs)

        url = f"{API_BASE_URL}{path}"
        try:
            resp = _requests.request(
                method, url, timeout=10,
                headers={"Content-Type": "application/json"},
                **kwargs,
            )
        except _requests.RequestException:
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
                "version": "6.0.0",
                "service": "Korea Compass",
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
                localize_items,
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
            display_results = localize_items(results, language=language)
            serialisable = []
            for item in display_results:
                item_copy = dict(item)
                item_copy["relevance_score"] = float(item_copy.get("relevance_score", 0))
                serialisable.append(item_copy)
            return {
                "results": serialisable,
                "ai_summary": generate_trend_summary(results, keyword, language=language),
                "action_suggestions": generate_action_suggestions(results, keyword, language=language),
                "result_count": len(serialisable),
            }

        if method == "GET" and path.startswith("/api/v1/explore/"):
            from backend.app.services import explore_service

            explore_routes = {
                "/api/v1/explore/overview": explore_service.get_overview,
                "/api/v1/explore/cities": explore_service.get_cities,
                "/api/v1/explore/culture": explore_service.get_culture,
                "/api/v1/explore/history": explore_service.get_history,
                "/api/v1/explore/living-cost": explore_service.get_living_cost,
                "/api/v1/explore/quick-facts": explore_service.get_quick_facts,
            }
            if path in explore_routes:
                return explore_routes[path]()

        if method == "GET" and path.startswith("/api/v1/korean-learning/"):
            from backend.app.services import korean_learning

            learning_routes = {
                "/api/v1/korean-learning/study": korean_learning.get_study_scenarios,
                "/api/v1/korean-learning/career": korean_learning.get_career_scenarios,
                "/api/v1/korean-learning/living": korean_learning.get_living_scenarios,
                "/api/v1/korean-learning/topik": korean_learning.get_topik_planners,
            }
            if path in learning_routes:
                return learning_routes[path]()

        if method == "POST" and path == "/api/v1/korean-learning/explain":
            from backend.app.services.korean_learning import explain_expression

            return explain_expression(
                expression=payload.get("expression", ""),
                action=payload.get("action", "explain_expression"),
                context=payload.get("context"),
            )

        if method == "GET" and path == "/api/v1/sources":
            from backend.app.services.source_registry import list_sources

            return list_sources()

        if method == "GET" and path == "/api/v1/sources/status":
            from backend.app.services.source_registry import validate_source

            return validate_source()

        if method == "GET" and path.startswith("/api/v1/sources/"):
            from backend.app.services.source_registry import get_source

            return get_source(path.rsplit("/", 1)[-1].replace("%20", " "))

        if method == "GET" and path == "/api/v1/kb/status":
            from backend.app.services.data_loader import validate_metadata

            return validate_metadata()

        if method == "POST" and path == "/api/v1/profiles":
            import datetime as _dt

            return {
                "id": 0,
                "display_name": payload.get("display_name") or "Compass User",
                "study_profile": payload.get("study_profile") or {},
                "career_profile": payload.get("career_profile") or {},
                "living_profile": payload.get("living_profile") or {},
                "created_at": _dt.datetime.utcnow().isoformat(),
            }

        if method == "GET" and path == "/api/v1/profiles/latest":
            return None

        if method == "POST" and path == "/api/v1/city-recommendations":
            from backend.app.services.city_recommendation import recommend_cities

            return recommend_cities(
                payload.get("study_profile") or {},
                payload.get("career_profile") or {},
                payload.get("living_profile") or {},
                language="zh" if payload.get("language") == "zh" else "en",
            )

        if method == "POST" and path == "/api/v1/korea-life-plan/generate":
            from backend.app.services.korea_life_plan import generate_korea_life_plan

            return generate_korea_life_plan(
                display_name=payload.get("display_name") or "Compass User",
                study_profile=payload.get("study_profile") or {},
                career_profile=payload.get("career_profile") or {},
                living_profile=payload.get("living_profile") or {},
                language="zh" if payload.get("language") == "zh" else "en",
            )

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

    # ── Explore Korea ──

    def get_explore_overview(self) -> dict:
        return self._request("GET", "/api/v1/explore/overview")

    def get_explore_cities(self) -> list[dict]:
        return self._request("GET", "/api/v1/explore/cities")

    def get_explore_culture(self) -> list[dict]:
        return self._request("GET", "/api/v1/explore/culture")

    def get_explore_history(self) -> list[dict]:
        return self._request("GET", "/api/v1/explore/history")

    def get_explore_living_cost(self) -> list[dict]:
        return self._request("GET", "/api/v1/explore/living-cost")

    def get_explore_quick_facts(self) -> list[dict]:
        return self._request("GET", "/api/v1/explore/quick-facts")

    # ── Korean Learning Support ──

    def get_korean_learning_study(self) -> list[dict]:
        return self._request("GET", "/api/v1/korean-learning/study")

    def get_korean_learning_career(self) -> list[dict]:
        return self._request("GET", "/api/v1/korean-learning/career")

    def get_korean_learning_living(self) -> list[dict]:
        return self._request("GET", "/api/v1/korean-learning/living")

    def get_korean_learning_topik(self) -> list[dict]:
        return self._request("GET", "/api/v1/korean-learning/topik")

    def explain_korean_expression(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/korean-learning/explain", json=payload)

    # ── Knowledge Base ──

    def get_kb_status(self) -> dict:
        return self._request("GET", "/api/v1/kb/status")

    def list_sources(self) -> list[dict]:
        return self._request("GET", "/api/v1/sources")

    def get_source(self, name: str) -> dict:
        return self._request("GET", f"/api/v1/sources/{name}")

    def get_sources_status(self) -> dict:
        return self._request("GET", "/api/v1/sources/status")

    # ── Korea Compass V3 ──

    def create_profile(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/profiles", json=payload)

    def get_latest_profile(self) -> Optional[dict]:
        return self._request("GET", "/api/v1/profiles/latest")

    def recommend_cities(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/city-recommendations", json=payload)

    def generate_korea_life_plan(self, payload: dict) -> dict:
        return self._request("POST", "/api/v1/korea-life-plan/generate", json=payload)

    def get_korea_life_plan_history(self, limit: int = 10) -> list[dict]:
        return self._request("GET", "/api/v1/korea-life-plan/history", params={"limit": limit})
