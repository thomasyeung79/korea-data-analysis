from typing import Optional

from fastapi import APIRouter, Query

from backend.app.services.data_service import load_kpop_data

router = APIRouter(prefix="/api/v1/kpop", tags=["kpop"])


def _get_generation(year: int) -> str:
    if year <= 2003:
        return "1st Gen"
    elif year <= 2011:
        return "2nd Gen"
    elif year <= 2017:
        return "3rd Gen"
    elif year <= 2021:
        return "4th Gen"
    else:
        return "5th Gen"


BIG4 = ["SM", "JYP", "YG", "HYBE"]

GLOBAL_MAINSTREAM = [
    "BTS", "BLACKPINK", "Stray Kids", "TWICE",
    "SEVENTEEN", "aespa", "NewJeans",
]
CURRENT_EXPANSION = [
    "TXT", "ENHYPEN", "LE SSERAFIM", "IVE", "RIIZE",
    "BABYMONSTER", "NMIXX", "BOYNEXTDOOR", "TWS", "ILLIT", "ZEROBASEONE",
]
EXPERIMENTAL_GLOBAL = [
    "NiziU", "NEXZ", "&TEAM", "WayV", "KATSEYE", "VCHA", "XG",
]
HISTORICAL_MODELS = [
    "TVXQ", "EXO", "Girls' Generation", "SUPER JUNIOR",
    "SHINee", "2PM", "2NE1", "BIGBANG", "Wonder Girls",
]


def _get_expansion_category(name: str) -> str:
    if name in GLOBAL_MAINSTREAM:
        return "Global Mainstream"
    elif name in CURRENT_EXPANSION:
        return "Current Expansion"
    elif name in EXPERIMENTAL_GLOBAL:
        return "Experimental Global"
    elif name in HISTORICAL_MODELS:
        return "Historical Expansion"
    return "Others"


@router.get("/artists")
def get_kpop_artists(
    artist_type: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    main_market: Optional[str] = Query(None),
    generation: Optional[str] = Query(None),
    expansion_category: Optional[str] = Query(None),
):
    data = load_kpop_data()
    if not data:
        return []

    result = []
    for row in data:
        gen = _get_generation(row.get("debut_year", 2020))
        exp_cat = _get_expansion_category(row.get("artist_name", ""))

        if artist_type and row.get("artist_type") != artist_type:
            continue
        if gender and row.get("gender") != gender:
            continue
        if main_market and row.get("main_market") != main_market:
            continue
        if generation and gen != generation:
            continue
        if expansion_category and exp_cat != expansion_category:
            continue

        result.append({
            **row,
            "generation": gen,
            "company_group": row.get("company") if row.get("company") in BIG4 else "Others",
            "expansion_category": exp_cat,
        })

    return result


@router.get("/metrics")
def get_kpop_metrics():
    data = load_kpop_data()
    if not data:
        return {}

    companies = set()
    markets = set()
    gens = set()
    for row in data:
        companies.add(row.get("company", "Unknown"))
        markets.add(row.get("main_market", "Unknown"))
        gens.add(_get_generation(row.get("debut_year", 2020)))

    return {
        "total_artists": len(data),
        "total_companies": len(companies),
        "total_markets": len(markets),
        "total_generations": len(gens),
    }


@router.get("/us-potential")
def get_us_potential():
    data = load_kpop_data()
    if not data:
        return []

    US_GLOBAL_TARGETS = GLOBAL_MAINSTREAM + CURRENT_EXPANSION + EXPERIMENTAL_GLOBAL
    SUPERSTARS = ["BTS", "BLACKPINK", "Stray Kids", "NewJeans", "aespa"]

    company_scores: dict[str, float] = {}

    for row in data:
        company = row.get("company", "Others")
        if company not in BIG4:
            company = "Others"

        if company not in company_scores:
            company_scores[company] = 0

        score = 0
        if row.get("main_market") in ("Global", "USA", "US"):
            score += 2
        if (row.get("debut_year") or 0) >= 2018:
            score += 1.5
        if row.get("artist_name") in US_GLOBAL_TARGETS:
            score += 2
        if row.get("artist_name") in SUPERSTARS:
            score += 5
        if row.get("artist_type") == "group":
            score += 1

        company_scores[company] = company_scores.get(company, 0) + score

    return sorted(
        [{"company": k, "us_potential_score": round(v, 2)} for k, v in company_scores.items()],
        key=lambda x: x["us_potential_score"],
        reverse=True,
    )


@router.get("/hit-predictor")
def get_hit_predictions():
    data = load_kpop_data()
    if not data:
        return []

    US_GLOBAL_TARGETS = GLOBAL_MAINSTREAM + CURRENT_EXPANSION + EXPERIMENTAL_GLOBAL
    candidates = []

    for row in data:
        score = 0
        if (row.get("debut_year") or 0) >= 2018:
            score += 3
        if row.get("main_market") in ("Global", "USA", "US"):
            score += 4
        if row.get("artist_type") == "group":
            score += 2
        if row.get("company") in BIG4:
            score += 2
        if _get_generation(row.get("debut_year", 2020)) == "5th Gen":
            score += 2

        exp_cat = _get_expansion_category(row.get("artist_name", ""))
        if exp_cat == "Global Mainstream":
            score += 4
        elif exp_cat == "Current Expansion":
            score += 3
        elif exp_cat == "Experimental Global":
            score += 2

        candidates.append({
            "artist_name": row.get("artist_name", "Unknown"),
            "company": row.get("company", "Unknown"),
            "company_group": row.get("company") if row.get("company") in BIG4 else "Others",
            "generation": _get_generation(row.get("debut_year", 2020)),
            "main_market": row.get("main_market", "Unknown"),
            "expansion_category": exp_cat,
            "global_hit_score": score,
        })

    return sorted(candidates, key=lambda x: x["global_hit_score"], reverse=True)
