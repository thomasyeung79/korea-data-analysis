import pandas as pd
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


@lru_cache(maxsize=3)
def load_kpop_data() -> list[dict]:
    path = DATA_DIR / "kpop_data.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


@lru_cache(maxsize=3)
def load_epl_data() -> list[dict]:
    path = DATA_DIR / "east_asian_epl_appearances.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


@lru_cache(maxsize=3)
def load_ucl_data() -> list[dict]:
    path = DATA_DIR / "east_asia_ucl_players_dataset_checked_split_by_club.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


def clear_cache():
    load_kpop_data.cache_clear()
    load_epl_data.cache_clear()
    load_ucl_data.cache_clear()
