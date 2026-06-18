# Korea Study & Career Decision Agent — V2 Product Plan

> **Repositioning Korea Analysis from a general perception tool into a focused AI assistant for Korea study, career, and living decisions.**

---

## 1. Product Positioning

### Product Name
**Korea Study & Career Decision Agent**  
(Internal code: KAS V2)

### One-Line Value Proposition
> *"One dashboard to answer: should I study, work, or live in Korea, and what should I prepare?"*

### Current State (V1)
Korea Analysis is a general-purpose perception measurement tool. Users compare Korea across 6 dimensions, submit perception surveys, and receive AI-generated perception reports. It answers *"How is Korea perceived?"*

### Target State (V2)
A practical decision-making assistant. Users input their personal profile (budget, skills, goals, language ability) and receive:
- **Study Cost Calculator** — "How much will it cost to study in Seoul/Busan?"
- **IT Job Market Analyzer** — "Can I get a job as a developer in Korea?"
- **News & Policy Summarizer** — "What changed in the D-10 visa this month?"
- **AI Decision Report** — "Should I choose Korea over Australia for my career?"

It answers *"Should I go to Korea, and how do I prepare?"*

### Why This Pivot?

| Problem with V1 | V2 Solution |
|----------------|-------------|
| "Interesting but I can't act on it" | Actionable cost, job, and visa data |
| "It's about perception, not practical information" | Practical decision-making focus |
| "I don't know Korea well enough to have a perception" | Meet users where they are — exploring the idea of Korea |
| "What do I do with this report?" | Each output includes a 3-month action plan |

---

## 2. Target Users

| Persona | Description | Primary Need |
|---------|-------------|-------------|
| **International Student Prospect** | 20–28, considering Korea for university | Study cost, scholarship info, city comparison |
| **IT Job Seeker** | 24–35, developer/designer/PM looking at Korea market | Salary ranges, Korean language requirement, visa pathways |
| **Career Changer** | 28–40, considering Korea vs Australia vs China | Decision report comparing countries |
| **K-Culture Fan → Realist** | 18–25, inspired by K-content to consider Korea seriously | Practical checklist, cost of living, culture shock prep |
| **Remote Worker / Digital Nomad** | 25–40, considering Korea as a base | Visa options, cost of living in different cities |

---

## 3. User Pain Points

| Pain Point | Current State | V2 Addresses |
|------------|--------------|--------------|
| **Scattered info** | Tuition, visa, salary data is spread across dozens of Korean government sites, blogs, forums | Centralised dashboard with curated, structured data |
| **Language barrier** | Most practical info is in Korean | English-first summarisation layer |
| **No personalised view** | Generic blog posts, not tailored to user's budget/skills | Personalised cost, salary, and decision reports |
| **Hard to compare** | "Korea vs Australia vs China" requires cross-referencing multiple sources | Side-by-side comparison in AI Decision Report |
| **No action plan** | Users read articles but don't know what to do next | Every output includes a preparation checklist + 3-month plan |
| **Outdated visa/policy info** | Word of mouth, forums | News + Policy summariser with keyword tracking |

---

## 4. Core Workflow

```
User arrives at app
         │
         ▼
   ┌──────────────────┐
   │  Landing Page     │  "Should I study, work, or live in Korea?"
   │  Goal Selector    │  ┌─ Study ─ Work ─ Live ─ Compare ┐
   └────────┬─────────┘
            │
     ┌──────┴──────┐
     ▼             ▼
┌──────────┐ ┌──────────┐
│ Study     │ │ IT Job   │
│ Cost      │ │ Market   │
│ Calculator│ │ Analyzer │
└─────┬────┘ └────┬─────┘
      │           │
      ▼           ▼
┌──────────┐ ┌──────────┐
│ Cost      │ │ Skills   │
│ Breakdown│ │ + Salary │
│ Chart     │ │ + Roadmap│
└─────┬────┘ └────┬─────┘
      │           │
      └──────┬────┘
             ▼
     ┌──────────────┐
     │ News & Policy │
     │ Summariser    │
     │ (Context layer)│
     └──────┬───────┘
            ▼
     ┌──────────────┐
     │ AI Decision  │
     │ Report       │
     │ "Korea vs    │
     │ Australia"   │
     └──────────────┘
```

---

## 5. MVP Feature List (4 Modules)

### Module 1: Korea Study Cost Calculator

**Inputs:**
- City: Seoul / Busan / Daegu / Daejeon / Incheon / Other
- School type: University (SKY) / National university / Private university / Graduate school / Language program
- Housing: Dormitory / One-room (monthly rent) / Goshiwon / Shared apartment
- Monthly lifestyle: Frugal / Moderate / Comfortable

**Outputs:**
- Estimated monthly cost (KRW → USD/AUD)
- Estimated annual cost
- Cost breakdown pie chart (tuition + housing + food + transport + insurance + misc)
- Comparison across 2–3 selected cities
- AI explanation of cost drivers
- Scholarship consideration notes

**Data sources:** In-house curated dataset (not real-time API for MVP). 50–100 data points covering major universities and city averages.

### Module 2: Korea IT Job Market Analysis

**Inputs:**
- Target role: Frontend / Backend / Full-Stack / Data / DevOps / PM / Design / QA
- Experience level: Junior (0–2) / Mid (3–5) / Senior (6–10) / Lead (10+)
- Korean language ability: None / Beginner / TOPIK 2 / TOPIK 3 / TOPIK 4 / TOPIK 5+ / Native
- Current country: Korea / Australia / China / Other
- Visa status: None (need sponsorship) / Student visa / F-2 / F-4 / F-6 / F-visa / Other

**Outputs:**
- Required skills matrix (must-have vs nice-to-have)
- Korean language requirement level for this role
- Expected salary range (KRW/year, with conversion to USD/AUD)
- Company types that hire foreigners (Startup / Chaebol / Foreign company / Gov research)
- Recommended preparation plan with timeline
- Comparison with same role in Australia (if selected)

**Data sources:** In-house curated dataset based on published salary surveys, job postings analysis. 30–50 role/level combinations.

### Module 3: Korea News & Policy Summary

**Inputs:**
- Keyword: free text (e.g. "D-10 visa", "scholarship 2026", "tech hiring")
- Category: Study / Work / Visa / Economy / Technology / Society / Culture
- Time period: Last week / Last month / Last 3 months

**Outputs:**
- 3–5 latest news/policy items summarised
- Key points for students or job seekers
- Impact assessment: "This change affects..."
- Source links (where available)

**Implementation notes:**
- MVP: Curated RSS/Atom feeds or manually updated JSON source
- Future: NewsAPI.org or Korean news API
- Each item: title, summary, source URL, category, date, impact tag

### Module 4: AI Decision Report

**Inputs (aggregated from previous modules + direct form):**
- Profile name / label
- Goal: Study / Work / Live
- Target country comparison: Korea vs Australia / Korea vs China / Korea vs US / Korea vs Japan
- Monthly budget
- Target city in Korea
- Korean language level
- Education level
- Years of work experience
- Risk tolerance: Low / Medium / High

**Outputs:**
- Personalised decision summary: "Korea is a strong match for you because..."
- Risk factors: "Things to be aware of..."
- Comparison highlights: "In Australia you would earn X% more but pay X% more in living costs"
- Preparation checklist (10–20 items, checkable)
- 3-month action plan (Month 1 / Month 2 / Month 3)
- Community context: "X% of surveyed users with similar profiles chose Korea"

**AI integration:** Uses existing dual-provider architecture (OpenAI + local fallback).

---

## 6. Database Schema

### New Tables

```sql
-- Study cost data points
CREATE TABLE study_costs (
    id INTEGER PRIMARY KEY,
    city TEXT NOT NULL,
    school_type TEXT NOT NULL,
    housing_type TEXT NOT NULL,
    lifestyle TEXT NOT NULL,
    tuition_annual_krw REAL,
    housing_monthly_krw REAL,
    food_monthly_krw REAL,
    transport_monthly_krw REAL,
    insurance_monthly_krw REAL,
    misc_monthly_krw REAL,
    currency TEXT DEFAULT 'KRW',
    source TEXT,
    updated_at TEXT
);

-- IT job market data points
CREATE TABLE job_market_data (
    id INTEGER PRIMARY KEY,
    role TEXT NOT NULL,
    experience_level TEXT NOT NULL,
    korean_level_required TEXT,
    salary_min_krw REAL,
    salary_max_krw REAL,
    salary_median_krw REAL,
    skill_requirements TEXT,       -- JSON array
    common_company_types TEXT,      -- JSON array
    visa_sponsorship_common BOOLEAN,
    korean_level_explanation TEXT,
    source TEXT,
    updated_at TEXT
);

-- News / policy items
CREATE TABLE news_items (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    category TEXT NOT NULL,
    keyword_tags TEXT,               -- JSON array
    impact_for_students TEXT,
    impact_for_job_seekers TEXT,
    source_url TEXT,
    source_name TEXT,
    published_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- City reference data
CREATE TABLE city_data (
    id INTEGER PRIMARY KEY,
    city TEXT NOT NULL UNIQUE,
    country TEXT DEFAULT 'Korea',
    avg_monthly_rent_krw REAL,
    avg_transport_monthly_krw REAL,
    avg_grocery_monthly_krw REAL,
    has_subway BOOLEAN,
    university_count INTEGER,
    tech_job_density TEXT     -- High / Medium / Low
);
```

### Existing Tables (Keep Unchanged)

- `country_scores` — Used by Comparison Lab (can remain)
- `perception_surveys` — Can remain, may be de-emphasised in V2 nav

---

## 7. API Design

### New Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/v1/study-costs` | Study cost data, filterable by city/school/housing |
| `GET` | `/api/v1/job-market` | Job market data, filterable by role/level |
| `GET` | `/api/v1/news` | News items, filterable by category/keyword |
| `GET` | `/api/v1/cities` | City reference data |
| `POST` | `/api/v1/ai/decision-report` | Generate AI Decision Report (aggregated) |

### Schema Additions

```python
class StudyCostRequest(BaseModel):
    city: str
    school_type: str
    housing_type: str
    lifestyle: str

class StudyCostResponse(BaseModel):
    estimated_monthly_total: float
    estimated_annual_total: float
    breakdown: dict          # {tuition, housing, food, transport, insurance, misc}
    currency: str
    comparison_with_other_cities: list[dict]

class JobMarketRequest(BaseModel):
    role: str
    experience_level: str
    korean_level: str

class JobMarketResponse(BaseModel):
    skills_required: list[str]
    skills_nice_to_have: list[str]
    korean_level_required: str
    salary_range: dict       # {min, max, median, currency}
    company_types: list[str]
    preparation_plan: dict   # {month1, month2, month3}

class DecisionReportRequest(BaseModel):
    goal: str                 # study / work / live
    target_country_comparison: str | None
    monthly_budget: float
    target_city: str
    korean_level: str
    education_level: str
    work_experience_years: int
    risk_tolerance: str       # low / medium / high

class DecisionReportResponse(BaseModel):
    decision_summary: str
    risk_factors: list[str]
    comparison_highlights: list[str]
    preparation_checklist: list[str]
    action_plan: dict          # {month1, month2, month3}
    community_context: str | None
```

---

## 8. Page Structure

### V2 Navigation Flow

```
Home (repositioned)
├── 📚 Study Cost Calculator    → pages/1_Study_Cost.py
├── 💻 IT Job Market Analyzer   → pages/2_Job_Market.py
├── 📰 Korea News & Policy      → pages/3_News.py
├── 🧭 AI Decision Report       → pages/4_Decision_Report.py
└── 📊 Country Comparison       → pages/5_Comparison.py (existing, de-prioritised)
```

### Page Descriptions

**1. Study Cost Calculator** `pages/1_Study_Cost.py`
- City selector, school type, housing type, lifestyle slider
- Results: monthly/ annual cost, breakdown pie chart, city comparison bar chart
- AI explanation box (optional toggle)
- Export to PDF / save button

**2. IT Job Market Analyzer** `pages/2_Job_Market.py`
- Role selector, experience level, language ability, current country
- Results: skills matrix, salary range chart, recommended preparation roadmap
- Compare with Australia toggle

**3. Korea News & Policy** `pages/3_News.py`
- Keyword search bar + category filter
- News cards with summary, impact tags, source link
- Keyword subscription (MVP: local session-based)

**4. AI Decision Report** `pages/4_Decision_Report.py`
- Full profile form (goal, budget, city, language, education, experience, risk tolerance)
- Option to compare Korea vs Australia / China / Japan
- Generate button → structured report with:
  - Decision summary card
  - Risk factors
  - Country comparison highlights
  - Preparation checklist (interactive)
  - 3-month action plan (styled timeline)
- Export to PDF / save

**Removed / Archived from main nav:**
- Perception Survey → moved to secondary footer link
- Community Insights → accessible from Decision Report context
- AI Insight → now embedded in each module's output

---

## 9. Success Metrics

| Metric | Target (3 months post-launch) | How to Measure |
|--------|-------------------------------|----------------|
| Study Cost Calculator completions | 100+ | API endpoint counter |
| IT Job Market searches | 80+ | API endpoint counter |
| AI Decision Reports generated | 50+ | API endpoint counter |
| Time on page (Decision Report) | > 2 min avg | Streamlit analytics |
| Return visits | > 20% | Session replay (if added) |
| GitHub stars | > 30 | Repository counter |
| Portfolio mentions | 5+ interviewers ask about it | Self-reported |
| Survey submissions | 30+ (V1 feature retained) | Survey stats endpoint |

---

## 10. 2-Week Development Roadmap

### Week 1 — Foundation + Read Modules

| Day | Focus | Deliverable |
|-----|-------|-------------|
| **Day 1** | Product scaffolding | Create new page structure, stub out 4 new modules. Reposition home page. |
| **Day 2** | DB models + seed data | `study_costs`, `job_market_data`, `city_data`, `news_items` tables. 50 seed data points for study costs. |
| **Day 3** | Study Cost API + page | `GET /api/v1/study-costs` endpoint with filters. `pages/1_Study_Cost.py` with form + results. |
| **Day 4** | Study Cost frontend | Pie chart, city comparison, AI explanation box. Polish form UX. |
| **Day 5** | Job Market API + seed data | `GET /api/v1/job-market` endpoint. 30 role/level seed rows. `pages/2_Job_Market.py` form. |
| **Day 6** | Job Market frontend | Skills matrix render, salary chart (Plotly), roadmap display. "Compare Australia" toggle. |
| **Day 7** | Buffer / polish | Fix edge cases. Test all 3 new API endpoints. |

### Week 2 — Decision Report + News + Integration

| Day | Focus | Deliverable |
|-----|-------|-------------|
| **Day 8** | News API + seed data | `GET /api/v1/news` endpoint. 20–30 curated news items. `pages/3_News.py` with cards + filters. |
| **Day 9** | Decision Report backend | `POST /api/v1/ai/decision-report`. AI prompt + local fallback. |
| **Day 10** | Decision Report frontend | `pages/4_Decision_Report.py` with full form + report render. |
| **Day 11** | Integration + navigation | Reposition home page to V2 flow. Add V1 features to footer. Update navigation labels. |
| **Day 12** | README + screenshots | Update README.md with V2 positioning. Take screenshots of all 4 new modules. |
| **Day 13** | Polish + test | Fix all edge cases. Test all endpoints with curl. Test all pages visually. |
| **Day 14** | GitHub release | Commit all changes. Tag v2.0.0. Push to GitHub. |

---

## 11. Resume Value

| Aspect | How It Looks on a Resume |
|--------|-------------------------|
| **Product thinking** | "Repositioned a data product from general analytics to a practical decision assistant" |
| **Full-stack** | "Built a 4-module decision platform with Streamlit + FastAPI + SQLite + OpenAI" |
| **Domain expertise** | "Designed data models for international education costs, IT job markets, and visa policy" |
| **AI integration** | "Implemented dual-provider architecture: OpenAI GPT-4o-mini with deterministic fallback" |
| **Data engineering** | "Curated and structured 100+ real-world data points across cost, salary, and policy domains" |
| **International UX** | "Built for English-speaking users navigating Korean systems — solved a real language gap" |

---

## 12. Interview Talking Points

| Question | How to Answer |
|----------|---------------|
| "Tell me about a project you're proud of." | "I built a decision assistant for people considering Korea for study or work. It aggregates cost, job market, and policy data into one dashboard and generates personalised AI reports with action plans." |
| "Why did you pivot from V1 to V2?" | "V1 was a general perception tool — interesting but not actionable. Users told me (through comments) they were considering Korea practically but couldn't find centralised info. I pivoted to solve that real need." |
| "How did you handle data quality?" | "I curated in-house datasets from published sources — university tuition pages, salary surveys, government visa portals. Every data point has a source field. For MVP this is sufficient; in production I'd add automated data refresh pipelines." |
| "Why dual AI provider?" | "The product should work fully offline. OpenAI gives richer reports, but the local fallback produces the same JSON structure. This decouples the frontend from API availability — a portfolio project that works every time is better than one that breaks on demo day." |
| "What would you do next?" | "Add real-time NewsAPI integration, user accounts to save decision reports, PDF export, and expand the job market data to cover more industries beyond IT." |

---

## 13. GitHub Issues Plan

### Issue 1: Update README & product positioning
- **Title:** `docs: reposition README for V2 — Korea Study & Career Decision Agent`
- **Description:** Rewrite README to reflect new product positioning. Update product name, tagline, feature list, screenshots, and roadmap. Keep V1 feature references but under a "Legacy" section.
- **Files:** `README.md`
- **Labels:** `documentation`

### Issue 2: Build Study Cost Calculator
- **Title:** `feat: add Study Cost Calculator module`
- **Description:** Implement Module 1. Includes:
  - New DB table `study_costs` with migration
  - Seed data (50+ rows covering major cities and school types)
  - API endpoint `GET /api/v1/study-costs`
  - Frontend page `pages/1_Study_Cost.py` with form, pie chart, and AI explanation
- **Files:** `backend/app/models.py`, `backend/app/schemas.py`, `backend/app/routers/study_costs.py`, `backend/app/main.py`, `pages/1_Study_Cost.py`, `api_client.py`
- **Labels:** `feature`

### Issue 3: Build IT Job Market Analysis
- **Title:** `feat: add IT Job Market Analyzer module`
- **Description:** Implement Module 2. Includes:
  - New DB table `job_market_data`
  - Seed data (30+ rows across role/level combinations)
  - API endpoint `GET /api/v1/job-market`
  - Frontend page `pages/2_Job_Market.py` with skills matrix, salary chart, roadmap
- **Files:** `backend/app/models.py`, `backend/app/schemas.py`, `backend/app/routers/job_market.py`, `pages/2_Job_Market.py`, `api_client.py`
- **Labels:** `feature`

### Issue 4: Build News Summary Module
- **Title:** `feat: add Korea News & Policy summariser`
- **Description:** Implement Module 3. Includes:
  - New DB table `news_items`
  - Seed data (20-30 curated news items across 4+ categories)
  - API endpoint `GET /api/v1/news` with keyword and category filters
  - Frontend page `pages/3_News.py` with search bar, category chips, card layout
- **Files:** `backend/app/models.py`, `backend/app/routers/news.py`, `pages/3_News.py`, `api_client.py`
- **Labels:** `feature`

### Issue 5: Build AI Decision Report
- **Title:** `feat: add AI Decision Report engine`
- **Description:** Implement Module 4. Includes:
  - API endpoint `POST /api/v1/ai/decision-report` with extended prompt
  - Local fallback provider for decision reports
  - Frontend page `pages/4_Decision_Report.py` with profile form, report display, checklist, action plan
- **Files:** `backend/app/ai/decision_provider.py`, `backend/app/ai/local_decision_provider.py`, `backend/app/routers/ai.py` (extend), `backend/app/schemas.py` (extend), `pages/4_Decision_Report.py`, `api_client.py`
- **Labels:** `feature`

### Issue 6: Add Charts and Export
- **Title:** `feat: add Plotly visualisations and PDF/CSV export`
- **Description:** Add charts to all modules: study cost pie + comparison bars, salary range chart, breakdown chart. Add CSV export for raw data tables. Add basic PDF export for Decision Report (using `reportlab` or `weasyprint`).
- **Files:** All 4 module pages, `api_client.py`
- **Labels:** `enhancement`

### Issue 7: Tests and Final Release Notes
- **Title:** `test: add tests for V2 modules and create v2.0.0 release`
- **Description:** Write pytest tests for all new API endpoints. Write business-rule tests for decision report fallback logic. Update CHANGELOG. Tag v2.0.0 release.
- **Files:** `tests/`, `CHANGELOG.md`
- **Labels:** `testing`, `release`

---

## 14. What Stays vs What Changes

| Component | V1 | V2 |
|-----------|----|----|
| Home page | Perception-focused hero, 4 nav cards | Decision-focused hero, 5 nav cards (4 new + 1 legacy) |
| Page 1 | Comparison Lab (radar chart) | **Study Cost Calculator** (new) |
| Page 2 | Perception Survey + AI Report | **IT Job Market Analyzer** (new) |
| Page 3 | Community Insights | **Korea News & Policy** (new) |
| Page 4 | — (AI Insight on Survey page) | **AI Decision Report** (new) |
| Page 5 | — | **Comparison Lab** (moved, de-prioritised) |
| AI endpoint | `/api/v1/ai/perception-report` | Keep + add `/api/v1/ai/decision-report` |
| Database | `country_scores`, `perception_surveys` | Keep both + add 4 new tables |
| `api_client.py` | 13 methods | Add 4-5 methods for new modules |
| README | Perception product | Decision assistant product |
| `app.py` | V1 navigation | V2 navigation + footer link to V1 features |

---

## 15. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data accuracy criticisms | Medium | High | Mark all data as "directional estimates". Source field on every row. Add disclaimer banner. |
| Users expect real-time data | High | Medium | Set expectations clearly: "Curated dataset, updated periodically." Add last-updated timestamp. |
| Scope creep (doing too much) | Medium | High | Strictly 4 modules for MVP. No chat, no RAG, no vector DB, no auth. |
| Losing existing users who liked V1 | Low | Low | Keep V1 features accessible via footer link. Don't break existing URLs. |
| AI Decision Report too generic | Medium | Medium | Local fallback uses structured templates; AI version uses detailed prompt with user data. |
| News data goes stale | High | Medium | Start with curated snapshot. Make it easy to add rows. Note "this is a sample" in MVP. |

---

## 16. V1 Features — What to Do With Them

| V1 Feature | V2 Decision |
|------------|-------------|
| **Comparison Lab** (radar, country scores) | Keep but move to secondary nav. It's good portfolio material but not the core. |
| **Perception Survey** | Keep but move to footer. Still generates data for "community context" in Decision Report. |
| **AI Perception Report** | Keep as-is. It works. Link from Decision Report as supplementary reading. |
| **Community Insights** | Keep but move to footer. The profile distribution data feeds the Decision Report's "community context" section. |

**Integration point:** The Decision Report can reference existing V1 data:
- "Community context: X% of surveyed users with your profile chose Korea" → uses Perception Survey stats
- "Korea's strongest dimension is Culture (9/10)" → uses CountryScore Korea baseline

---

*End of V2 Product Plan. Ready for implementation Day 1.*
