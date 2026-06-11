from typing import Dict, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..ai.local_provider import LocalReportProvider
from ..database import get_db
from ..models import CountryScore, PerceptionSurvey
from ..schemas import (
    PerceptionSurveyCreate,
    PerceptionSurveyResponse,
    PerceptionSurveyStats,
)

router = APIRouter(prefix="/api/v1/perception-surveys", tags=["perception surveys"])

CATEGORY_FIELDS = {
    "Economy": "economy_score",
    "Technology": "technology_score",
    "Education": "education_score",
    "Culture": "culture_score",
    "Global Influence": "global_influence_score",
    "Quality of Life": "quality_of_life_score",
}

FALLBACK_KOREA_BASELINE = {
    "Economy": 8.0,
    "Technology": 9.0,
    "Education": 8.0,
    "Culture": 9.0,
    "Global Influence": 8.0,
    "Quality of Life": 7.0,
}

COMMUNITY_CATEGORY_FIELDS = {
    "economy": "economy_score",
    "technology": "technology_score",
    "education": "education_score",
    "culture": "culture_score",
    "global_influence": "global_influence_score",
    "quality_of_life": "quality_of_life_score",
}

COMMUNITY_PROFILES = [
    "Soft Power Enthusiast",
    "Technology-Focused Analyst",
    "Market-Driven Pragmatist",
    "Balanced Regional Observer",
    "Quality-of-Life Skeptic",
]


def _to_response(survey: PerceptionSurvey) -> PerceptionSurveyResponse:
    return PerceptionSurveyResponse(
        id=survey.id,
        display_name=survey.display_name,
        economy_score=survey.economy_score,
        technology_score=survey.technology_score,
        education_score=survey.education_score,
        culture_score=survey.culture_score,
        global_influence_score=survey.global_influence_score,
        quality_of_life_score=survey.quality_of_life_score,
        comment=survey.comment,
        created_at=survey.created_at.isoformat() if survey.created_at else None,
    )


def _korea_baseline(db: Session) -> Dict[str, float]:
    rows = (
        db.query(CountryScore)
        .filter(CountryScore.country == "Korea")
        .order_by(CountryScore.year.desc())
        .all()
    )
    baseline = dict(FALLBACK_KOREA_BASELINE)
    for row in rows:
        if row.category in baseline:
            baseline[row.category] = float(row.score)
    return baseline


@router.post("", response_model=PerceptionSurveyResponse)
def create_perception_survey(
    data: PerceptionSurveyCreate,
    db: Session = Depends(get_db),
):
    survey = PerceptionSurvey(
        display_name=data.display_name or "Anonymous",
        economy_score=data.economy_score,
        technology_score=data.technology_score,
        education_score=data.education_score,
        culture_score=data.culture_score,
        global_influence_score=data.global_influence_score,
        quality_of_life_score=data.quality_of_life_score,
        comment=data.comment,
    )
    db.add(survey)
    db.commit()
    db.refresh(survey)
    return _to_response(survey)


@router.get("", response_model=List[PerceptionSurveyResponse])
def list_perception_surveys(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    surveys = (
        db.query(PerceptionSurvey)
        .order_by(PerceptionSurvey.created_at.desc(), PerceptionSurvey.id.desc())
        .limit(limit)
        .all()
    )
    return [_to_response(survey) for survey in surveys]


@router.get("/stats", response_model=PerceptionSurveyStats)
def get_perception_survey_stats(db: Session = Depends(get_db)):
    surveys = db.query(PerceptionSurvey).all()
    baseline = _korea_baseline(db)

    if not surveys:
        return PerceptionSurveyStats(
            total_submissions=0,
            average_score=None,
            average_by_category={},
            strongest_category=None,
            weakest_category=None,
            korea_baseline=baseline,
        )

    average_by_category = {}
    for category, field_name in CATEGORY_FIELDS.items():
        average_by_category[category] = round(
            sum(getattr(survey, field_name) for survey in surveys) / len(surveys),
            2,
        )

    all_values = [
        getattr(survey, field_name)
        for survey in surveys
        for field_name in CATEGORY_FIELDS.values()
    ]
    average_score = round(sum(all_values) / len(all_values), 2)
    strongest_category = max(average_by_category, key=average_by_category.get)
    weakest_category = min(average_by_category, key=average_by_category.get)

    return PerceptionSurveyStats(
        total_submissions=len(surveys),
        average_score=average_score,
        average_by_category=average_by_category,
        strongest_category=strongest_category,
        weakest_category=weakest_category,
        korea_baseline=baseline,
    )


@router.get("/community-summary")
def get_community_summary(db: Session = Depends(get_db)):
    surveys = db.query(PerceptionSurvey).all()
    profile_distribution = {profile: 0 for profile in COMMUNITY_PROFILES}

    if not surveys:
        return {
            "total_responses": 0,
            "average_score": 0.0,
            "category_averages": {
                category: 0.0 for category in COMMUNITY_CATEGORY_FIELDS
            },
            "strongest_category": "",
            "weakest_category": "",
            "profile_distribution": profile_distribution,
            "recent_comments": [],
        }

    category_averages = {
        category: round(
            sum(getattr(survey, field_name) for survey in surveys) / len(surveys),
            2,
        )
        for category, field_name in COMMUNITY_CATEGORY_FIELDS.items()
    }
    all_scores = [
        getattr(survey, field_name)
        for survey in surveys
        for field_name in COMMUNITY_CATEGORY_FIELDS.values()
    ]

    profile_provider = LocalReportProvider()
    for survey in surveys:
        scores = {
            category: getattr(survey, field_name)
            for category, field_name in COMMUNITY_CATEGORY_FIELDS.items()
        }
        profile = profile_provider._profile_label(scores)
        if profile == "Culture-Driven Korea Optimist":
            profile = "Soft Power Enthusiast"
        profile_distribution[profile] += 1

    recent_comments = [
        survey.comment.strip()
        for survey in sorted(
            surveys,
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if survey.comment and survey.comment.strip()
    ][:20]

    return {
        "total_responses": len(surveys),
        "average_score": round(sum(all_scores) / len(all_scores), 2),
        "category_averages": category_averages,
        "strongest_category": max(category_averages, key=category_averages.get),
        "weakest_category": min(category_averages, key=category_averages.get),
        "profile_distribution": profile_distribution,
        "recent_comments": recent_comments,
    }
