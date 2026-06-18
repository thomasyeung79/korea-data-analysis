# Korea Analysis V2 — Internationalization (i18n) Design

> **Phase 1 scope:** English (default) + Simplified Chinese  
> **Goal:** Make all Streamlit frontend pages bilingual without changing business logic, APIs, or database schemas.

---

## 1. Language Switcher UX

### Placement
A single `st.selectbox` at the top of the page, below the hero section but before the form/content:
- **Option 1:** In the hero aside panel (consistent with V1 `app.py` pattern)
- **Option 2:** Fixed position near the top-right of the page

**Recommendation:** Option 1 — place the language selector in the hero aside or as the first interactive element after the hero, so it's visible immediately on every page.

### Behavior
- Default: `"English"`
- On change: update `st.session_state["language"]` → page re-runs automatically (Streamlit behavior)
- No page reload, no API call
- Selection persists within the session only (no backend storage for V1)

### Visual
```
[English  ▼]    ← selectbox, compact width
  English
  简体中文
```

---

## 2. Translation File Structure

### Recommended: Single Python module (no JSON files)

```python
# locales/i18n.py

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "page.title.home": {
        "en": "Korea Analysis",
        "zh": "韩国分析",
    },
    "hero.heading": {
        "en": "Should I study, work, or live in Korea?",
        "zh": "我该去韩国留学、工作还是生活？",
    },
    ...
}
```

**Why not JSON?**
- JSON cannot contain f-string placeholders
- JSON cannot contain comments for translators
- Python dict supports dynamic interpolation via `.format()` or `%` operators
- Single import in each page file: `from locales.i18n import t`

### Fallback behavior
```python
def t(key: str, lang: str = "en", **kwargs) -> str:
    """Translate a key. Falls back to English if translation missing."""
    entry = _TRANSLATIONS.get(key, {})
    text = entry.get(lang) or entry.get("en") or key
    if kwargs:
        return text.format(**kwargs)
    return text
```

**Fallback chain:** requested language → English → raw key (last resort)

---

## 3. Key Naming Conventions

Use dot-separated hierarchical keys:

| Pattern | Example |
|---------|---------|
| `page.<name>.title` | `page.study_cost.title` |
| `page.<name>.heading` | `page.decision_report.heading` |
| `page.<name>.label.<field>` | `page.study_cost.label.city` |
| `page.<name>.button.<action>` | `page.study_cost.button.calculate` |
| `page.<name>.metric.<name>` | `page.study_cost.metric.monthly` |
| `page.<name>.section.<name>` | `page.study_cost.section.breakdown` |
| `page.<name>.chart.<name>` | `page.study_cost.chart.pie_title` |
| `page.<name>.export.<name>` | `page.study_cost.export.download_csv` |
| `page.<name>.error.<condition>` | `page.study_cost.error.failed` |
| `page.<name>.empty.<condition>` | `page.study_cost.empty.no_results` |
| `common.<name>` | `common.back_to_home`, `common.export` |
| `common.metric.<name>` | `common.metric.monthly_cost` |
| `hero.<name>` | `hero.heading`, `hero.subtitle` |
| `flow.step<N>.<name>` | `flow.step1.title`, `flow.step1.desc` |
| `module.<name>.<field>` | `module.study_cost.title`, `module.job_market.desc` |

---

## 4. Files to Create / Modify

| File | Action |
|------|--------|
| `locales/__init__.py` | NEW — empty |
| `locales/i18n.py` | NEW — translation dictionary + `t()` function |
| `app.py` | MODIFY — add language selector, wrap ~42 strings |
| `pages/1_Study_Cost.py` | MODIFY — wrap ~35 strings |
| `pages/2_Job_Market.py` | MODIFY — wrap ~37 strings |
| `pages/3_Decision_Report.py` | MODIFY — wrap ~42 strings |
| `pages/4_News_Policy.py` | MODIFY — wrap ~30 strings |
| `pages/1_Comparison_Lab.py` | MODIFY — wrap ~20 strings |
| `pages/2_Perception_Survey.py` | MODIFY — wrap ~44 strings |
| `pages/3_Community_Insights.py` | MODIFY — wrap ~24 strings |
| `ui_style.py` | NO CHANGE — 0 strings |
| `api_client.py` | NO CHANGE — 1 string, backend error is English-only |
| `tests/` | NO CHANGE — no new tests needed |

---

## 5. Strings Requiring Translation by File

| File | Count | Notes |
|------|-------|-------|
| `app.py` | 42 | Hero, demo flow, nav cards, legacy buttons |
| `pages/1_Study_Cost.py` | 35 | Form labels, chart titles, export, footer |
| `pages/2_Job_Market.py` | 37 | Form labels, skills matrix, visa, export |
| `pages/3_Decision_Report.py` | 42 | Form, risk labels, export, action plan |
| `pages/4_News_Policy.py` | 30 | Search form, chart titles, result cards |
| `pages/1_Comparison_Lab.py` | 20 | Radar chart labels, data table |
| `pages/2_Perception_Survey.py` | 44 | Slider labels, AI report sections, stats |
| `pages/3_Community_Insights.py` | 24 | KPIs, chart labels, recent voices |
| **Total** | **274** | |

### Excluded from translation

| Category | Reason |
|----------|--------|
| City names (Seoul, Busan, etc.) | Proper nouns |
| Role names (Data Analyst, Backend Developer, etc.) | Industry-standard English terms |
| TOPIK levels (TOPIK 3, TOPIK 4, TOPIK 5+) | Standardised test names |
| School types (Language School, Undergraduate, Graduate School) | Consistent across both languages for searchability |
| Housing types (Dormitory, Shared Apartment, Studio Apartment) | Standard categories |
| Lifestyle levels (Budget, Standard, Premium) | Standard labels |
| API responses | Backend data, not frontend text |
| Database values | Not user-facing |
| File names (`korea_study_cost.csv`, etc.) | Machine-readable |
| Emoji icons (📚, 💻, 🧭, 📰, etc.) | Universal |
| CSS class names | Code |

---

## 6. Implementation Sequence (7 Issues)

### Issue 1: Build i18n utility
- Create `locales/__init__.py` (empty)
- Create `locales/i18n.py` with:
  - `_TRANSLATIONS` dict with ALL 274 keys (English only initially? or full bilingual?)
  - `t(key, **kwargs)` function with fallback
  - `get_language()` helper reading from `st.session_state`
- **Estimated effort:** 30 min (dictionary) + 15 min (function) = 45 min
- **Strings:** 0 (utility only)

### Issue 2: Add language switcher
- Modify `app.py` — add language selector in hero aside
- Each V2 page — add language selector near the top
- Modify `get_language()` pattern: if no session state, default to "en"
- **Estimated effort:** 20 min
- **Files:** `app.py` + 4 V2 pages + 3 V1 legacy pages

### Issue 3: Translate Study Cost page
- Wrap all 35 strings in `pages/1_Study_Cost.py` with `t()`
- Test: English and Chinese both render correctly
- **Estimated effort:** 30 min
- **Strings:** 35

### Issue 4: Translate Job Market page
- Wrap all 37 strings in `pages/2_Job_Market.py` with `t()`
- **Estimated effort:** 30 min
- **Strings:** 37

### Issue 5: Translate Decision Report page
- Wrap all 42 strings in `pages/3_Decision_Report.py` with `t()`
- **Estimated effort:** 35 min
- **Strings:** 42

### Issue 6: Translate News & Policy page
- Wrap all 30 strings in `pages/4_News_Policy.py` with `t()`
- Plus wrap V1 legacy pages (Comparison Lab ~20, Perception Survey ~44, Community Insights ~24)
- **Estimated effort:** 45 min (V2) + 40 min (V1 legacy) = 85 min
- **Strings:** 30 + 88 = 118

### Issue 7: Update README
- Add i18n section
- Document language switcher
- Update project structure
- **Estimated effort:** 10 min

---

## 7. Migration Effort Summary

| Metric | Value |
|--------|-------|
| Files to modify | 8 (app.py + 7 pages) |
| Files to create | 2 (locales/__init__.py, locales/i18n.py) |
| Total strings | ~274 |
| Interpolated strings | ~60 (need `t(key, lang=..., city=xxx)`) |
| Simple strings | ~214 (direct lookup, no args) |
| Estimated total time | 4-5 hours |
| Developer days | 1 day |

### Implementation pattern (per page)

**Before:**
```python
st.markdown("## Where your money goes")
st.selectbox("City", ["Seoul", "Busan", ...])
st.metric("Monthly (KRW)", f"{cost:,} ₩")
```

**After:**
```python
from locales.i18n import t, LANG
st.markdown(f"## {t('page.study_cost.heading.breakdown', lang=LANG)}")
st.selectbox(t("page.study_cost.label.city", lang=LANG), ["Seoul", "Busan", ...])
st.metric(t("page.study_cost.metric.monthly", lang=LANG), f"{cost:,} ₩")
```

City names, roles, TOPIK levels remain untranslated in the option list — they are proper nouns and standardised labels.

---

## 8. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Chinese translations may be inaccurate | Medium | Use common translations; avoid idiomatic phrases. Flag for native speaker review. |
| Page reruns on language switch cause flicker | Low | Streamlit reruns on every interaction anyway; this is standard behaviour. |
| Some strings missed (not wrapped in `t()`) | Medium | Run a grep for `st\.(markdown|metric|selectbox|button|info|error|success|warning|caption|subheader|title)`, audit each call. |
| Long Chinese text breaks layout | Medium | CSS `max-width` and `white-space` already handle this. Test with longest Chinese translations. |
| Export file contents in English | Low — Acceptable | File names remain English. Export content can remain English for portability. |

---

## 9. GitHub Issues

### Issue 1: Build i18n utility
- **Title:** `feat: add i18n utility (locales/i18n.py)`
- **Files:** `locales/__init__.py`, `locales/i18n.py`
- **Labels:** `i18n`
- **Effort:** 45 min

### Issue 2: Add language switcher
- **Title:** `feat: add language switcher to all pages`
- **Files:** All 8 page files
- **Labels:** `i18n`
- **Effort:** 20 min
- **Depends on:** Issue 1

### Issue 3-6: Translate pages
- **Titles:** `i18n: translate Study Cost / Job Market / Decision Report / News & Policy`
- **Files:** 1 page each
- **Labels:** `i18n`
- **Effort:** 30-45 min each
- **Depends on:** Issue 1 + 2

### Issue 7: Update README
- **Title:** `docs: update README with i18n documentation`
- **Labels:** `documentation`
- **Effort:** 10 min
