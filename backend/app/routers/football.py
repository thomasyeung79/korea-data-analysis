from typing import Optional

from fastapi import APIRouter, Query

from backend.app.services.data_service import load_epl_data, load_ucl_data

router = APIRouter(prefix="/api/v1/football", tags=["football"])

BIG6 = [
    "Manchester United", "Manchester City", "Liverpool",
    "Arsenal", "Chelsea", "Tottenham Hotspur",
]


@router.get("/epl")
def get_epl_data(
    country: Optional[str] = Query(None),
    player_type: Optional[str] = Query(None),
    competition_type: Optional[str] = Query(None),
):
    data = load_epl_data()
    if not data:
        return []

    result = []
    for row in data:
        if country and row.get("country") != country:
            continue
        if player_type and row.get("player_type") != player_type:
            continue
        if competition_type and row.get("competition_type") != competition_type:
            continue
        result.append({
            **row,
            "big6": row.get("club") in BIG6,
        })

    return result


@router.get("/ucl")
def get_ucl_data(
    country: Optional[str] = Query(None),
    ucl_status: Optional[str] = Query(None),
    confidence: Optional[str] = Query(None),
):
    data = load_ucl_data()
    if not data:
        return []

    result = []
    for row in data:
        if country and row.get("country") != country:
            continue
        if ucl_status and row.get("ucl_status") != ucl_status:
            continue
        if confidence and str(row.get("confidence", "")).lower() != confidence.lower():
            continue
        result.append(row)

    return result


@router.get("/epl/korea")
def get_korea_epl():
    data = load_epl_data()
    if not data:
        return []

    korea_data = [r for r in data if r.get("country") == "Korea"]
    return [{**r, "big6": r.get("club") in BIG6} for r in korea_data]


@router.get("/ucl/korea")
def get_korea_ucl():
    data = load_ucl_data()
    if not data:
        return []
    return [r for r in data if r.get("country") == "Korea"]


@router.get("/epl/big6")
def get_big6_summary():
    data = load_epl_data()
    if not data:
        return {}

    from collections import defaultdict
    summary: dict[str, dict[str, int]] = defaultdict(lambda: {"big6": 0, "non_big6": 0})

    for row in data:
        country = row.get("country", "Unknown")
        is_big6 = row.get("club") in BIG6
        if is_big6:
            summary[country]["big6"] += 1
        else:
            summary[country]["non_big6"] += 1

    return dict(summary)


@router.get("/insight")
def get_football_insight():
    epl_data = load_epl_data()
    ucl_data = load_ucl_data()

    epl_top_country = "N/A"
    epl_players = 0
    epl_big6_players = 0
    ucl_top_country = "N/A"
    ucl_players = 0
    appeared_players = 0

    if epl_data:
        from collections import Counter
        country_counts = Counter(r.get("country", "Unknown") for r in epl_data)
        if country_counts:
            epl_top_country = country_counts.most_common(1)[0][0]
        epl_players = len(set(r.get("player_name") for r in epl_data))
        epl_big6_players = len(set(
            r.get("player_name") for r in epl_data if r.get("club") in BIG6
        ))

    if ucl_data:
        from collections import Counter
        country_counts = Counter(r.get("country", "Unknown") for r in ucl_data)
        if country_counts:
            ucl_top_country = country_counts.most_common(1)[0][0]
        ucl_players = len(set(r.get("player_name") for r in ucl_data))
        appeared_players = len(set(
            r.get("player_name") for r in ucl_data
            if str(r.get("ucl_status", "")).lower() == "appeared"
        ))

    return {
        "epl_top_country": epl_top_country,
        "epl_unique_players": epl_players,
        "epl_big6_players": epl_big6_players,
        "ucl_top_country": ucl_top_country,
        "ucl_unique_players": ucl_players,
        "ucl_appeared_players": appeared_players,
    }
