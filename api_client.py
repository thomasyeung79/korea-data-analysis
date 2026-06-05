"""
API client for Streamlit pages to communicate with the FastAPI backend.
Handles JWT authentication and provides methods for all API endpoints.
"""
import json
from typing import Any, Optional

import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"


class APIClient:
    """API client with JWT token management via Streamlit session_state."""

    def __init__(self):
        self.token = st.session_state.get("jwt_token")
        self.user = st.session_state.get("user")

    @property
    def is_authenticated(self) -> bool:
        return bool(self.token) and bool(self.user)

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _request(
        self, method: str, path: str, **kwargs
    ) -> Any:
        url = f"{API_BASE_URL}{path}"
        try:
            resp = requests.request(method, url, headers=self._headers(), timeout=30, **kwargs)
        except requests.ConnectionError:
            st.error("Cannot connect to backend. Please ensure the backend server is running.")
            st.stop()

        if resp.status_code == 401:
            st.session_state.pop("jwt_token", None)
            st.session_state.pop("user", None)
            st.session_state.pop("api_client", None)
            st.error("Session expired. Please log in again.")
            st.rerun()
            st.stop()

        if resp.status_code >= 400:
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                detail = resp.text
            st.error(f"API Error ({resp.status_code}): {detail}")
            st.stop()

        if resp.status_code == 204:
            return None

        return resp.json()

    # ── Auth ──

    def register(self, username: str, password: str) -> dict:
        data = self._request("POST", "/api/v1/auth/register", json={
            "username": username,
            "password": password,
        })
        st.session_state["jwt_token"] = data["access_token"]
        st.session_state["user"] = data["user"]
        self.token = data["access_token"]
        self.user = data["user"]
        return data

    def login(self, username: str, password: str) -> dict:
        data = self._request("POST", "/api/v1/auth/login", json={
            "username": username,
            "password": password,
        })
        st.session_state["jwt_token"] = data["access_token"]
        st.session_state["user"] = data["user"]
        self.token = data["access_token"]
        self.user = data["user"]
        return data

    def get_profile(self) -> dict:
        return self._request("GET", "/api/v1/auth/me")

    def update_language(self, language: str) -> dict:
        data = self._request("PUT", "/api/v1/auth/language", json={
            "language_preference": language,
        })
        if self.user:
            self.user["language_preference"] = language
            st.session_state["user"] = self.user
        return data

    def logout(self):
        st.session_state.pop("jwt_token", None)
        st.session_state.pop("user", None)
        st.session_state.pop("api_client", None)
        self.token = None
        self.user = None

    # ── Module Scores ──

    def get_module_scores(self) -> list[dict]:
        return self._request("GET", "/api/v1/modules")

    def save_module_score(self, module_name: str, score: float) -> dict:
        return self._request("POST", "/api/v1/modules", json={
            "module_name": module_name,
            "score": score,
        })

    # ── Perception Results ──

    def get_perception_results(self) -> list[dict]:
        return self._request("GET", "/api/v1/perception")

    def save_perception_result(self, data: dict) -> dict:
        return self._request("POST", "/api/v1/perception", json=data)

    def get_latest_perception(self) -> dict:
        return self._request("GET", "/api/v1/perception/latest")

    # ── Travel Orders ──

    def get_travel_orders(self) -> list[dict]:
        return self._request("GET", "/api/v1/travel/orders")

    def create_travel_order(self, data: dict) -> dict:
        return self._request("POST", "/api/v1/travel/orders", json=data)

    def get_travel_order(self, order_id: str) -> dict:
        return self._request("GET", f"/api/v1/travel/orders/{order_id}")

    def delete_travel_order(self, order_id: str):
        self._request("DELETE", f"/api/v1/travel/orders/{order_id}")

    def get_travel_analytics(self) -> dict:
        return self._request("GET", "/api/v1/travel/analytics")

    def update_travel_order(self, order_id: str, data: dict) -> dict:
        return self._request("PUT", f"/api/v1/travel/orders/{order_id}", json=data)

    # ── K-pop Data ──

    def get_kpop_artists(self, filters: Optional[dict] = None) -> list[dict]:
        params = filters or {}
        return self._request("GET", "/api/v1/kpop/artists", params=params)

    def get_kpop_metrics(self) -> dict:
        return self._request("GET", "/api/v1/kpop/metrics")

    def get_kpop_us_potential(self) -> list[dict]:
        return self._request("GET", "/api/v1/kpop/us-potential")

    def get_kpop_hit_predictor(self) -> list[dict]:
        return self._request("GET", "/api/v1/kpop/hit-predictor")

    # ── Football Data ──

    def get_epl_data(self, filters: Optional[dict] = None) -> list[dict]:
        params = filters or {}
        return self._request("GET", "/api/v1/football/epl", params=params)

    def get_ucl_data(self, filters: Optional[dict] = None) -> list[dict]:
        params = filters or {}
        return self._request("GET", "/api/v1/football/ucl", params=params)

    def get_korea_epl(self) -> list[dict]:
        return self._request("GET", "/api/v1/football/epl/korea")

    def get_korea_ucl(self) -> list[dict]:
        return self._request("GET", "/api/v1/football/ucl/korea")

    def get_big6_summary(self) -> dict:
        return self._request("GET", "/api/v1/football/epl/big6")

    def get_football_insight(self) -> dict:
        return self._request("GET", "/api/v1/football/insight")

    # ── AI Proxy ──

    def generate_ai(self, prompt_type: str, params: dict) -> str:
        data = self._request("POST", "/api/v1/ai/generate", json={
            "prompt_type": prompt_type,
            "params": params,
        })
        return data.get("result", "")

    def chat_ai(self, message: str, history: Optional[list] = None) -> str:
        data = self._request("POST", "/api/v1/ai/chat", json={
            "message": message,
            "history": history or [],
        })
        return data.get("reply", "")

    # ── Auth extras ──

    def change_password(self, old_password: str, new_password: str) -> dict:
        return self._request("PUT", "/api/v1/auth/password", json={
            "old_password": old_password,
            "new_password": new_password,
        })

    # ── Perception extras ──

    def get_perception_averages(self) -> dict:
        return self._request("GET", "/api/v1/perception/averages")


def get_api() -> APIClient:
    """Get the API client from session_state, creating one if needed."""
    if "api_client" not in st.session_state:
        st.session_state["api_client"] = APIClient()
    return st.session_state["api_client"]
