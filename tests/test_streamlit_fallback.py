import requests

import api_client


def _offline_request(*args, **kwargs):
    raise requests.ConnectionError("offline")


def test_streamlit_fallback_health(monkeypatch):
    monkeypatch.setattr(api_client._requests, "request", _offline_request)

    result = api_client.APIClient().health()

    assert result["status"] == "ok"
    assert result["mode"] == "streamlit-local"


def test_streamlit_fallback_skips_http_when_api_base_url_missing(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("HTTP request should not be called without API_BASE_URL")

    monkeypatch.setattr(api_client, "API_BASE_URL", None)
    monkeypatch.setattr(api_client._requests, "request", fail_if_called)

    result = api_client.APIClient().health()

    assert result["mode"] == "streamlit-local"


def test_streamlit_fallback_study_cost(monkeypatch):
    monkeypatch.setattr(api_client._requests, "request", _offline_request)

    result = api_client.APIClient().calculate_study_cost(
        city="Seoul",
        school_type="Language School",
        housing_type="Dormitory",
        lifestyle_level="Budget",
        language="zh",
    )

    assert result["monthly_cost"] > 0
    assert result["breakdown"]
    assert "月度费用明细" in result["ai_summary"]


def test_streamlit_fallback_job_market(monkeypatch):
    monkeypatch.setattr(api_client._requests, "request", _offline_request)

    result = api_client.APIClient().analyze_job_market(
        role="Marketing Specialist",
        experience_level="0-2 years",
        korean_level="TOPIK 4",
        language="zh",
    )

    assert "数字营销" in result["required_skills"]
    assert "韩国市场案例库" in result["ai_plan"]


def test_streamlit_fallback_decision_report(monkeypatch):
    monkeypatch.setattr(api_client._requests, "request", _offline_request)

    result = api_client.APIClient().generate_decision_report(
        {
            "goal": "Work",
            "target_city": "Seoul",
            "school_type": "Not Applicable",
            "housing_type": "Not Applicable",
            "lifestyle_level": "Standard",
            "target_role": "Backend Developer",
            "experience_level": "0-2 years",
            "korean_level": "TOPIK 4",
            "monthly_budget": 2_000_000,
            "language": "zh",
        }
    )

    assert result["recommendation"]
    assert result["summary"]
    assert result["action_plan"]


def test_streamlit_fallback_news_policy(monkeypatch):
    monkeypatch.setattr(api_client._requests, "request", _offline_request)

    result = api_client.APIClient().search_news_policy(
        keyword="visa",
        category="All",
        time_range="Last 30 days",
        language="zh",
    )

    assert "results" in result
    assert "ai_summary" in result
    assert isinstance(result["action_suggestions"], list)
