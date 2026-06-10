import streamlit as st


def apply_product_style():
    st.markdown(
        """
<style>
:root {
    --ks-bg: #f5f7fb;
    --ks-surface: #ffffff;
    --ks-surface-soft: #f8fafc;
    --ks-text: #111827;
    --ks-muted: #64748b;
    --ks-line: #dbe3ef;
    --ks-red: #d7263d;
    --ks-blue: #123c9c;
    --ks-green: #0f9f6e;
    --ks-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

#MainMenu,
footer {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(215, 38, 61, 0.08), transparent 26rem),
        radial-gradient(circle at top right, rgba(18, 60, 156, 0.08), transparent 24rem),
        var(--ks-bg);
    color: var(--ks-text);
}

.block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    letter-spacing: 0;
}

div[data-testid="stMetric"] {
    background: var(--ks-surface);
    border: 1px solid var(--ks-line);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
}

.stButton > button {
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    background: var(--ks-surface);
    color: var(--ks-text);
    font-weight: 700;
    min-height: 2.75rem;
}

.stButton > button:hover {
    border-color: var(--ks-blue);
    color: var(--ks-blue);
}

.stButton > button[kind="primary"] {
    background: var(--ks-blue);
    color: white;
    border-color: var(--ks-blue);
}

.product-shell {
    border: 1px solid var(--ks-line);
    background: rgba(255, 255, 255, 0.88);
    box-shadow: var(--ks-shadow);
    border-radius: 8px;
    padding: 1.25rem;
}

.product-hero {
    display: grid;
    grid-template-columns: minmax(0, 1.45fr) minmax(280px, 0.75fr);
    gap: 1.4rem;
    align-items: stretch;
    margin-bottom: 1.25rem;
}

.hero-panel {
    border: 1px solid var(--ks-line);
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    border-radius: 8px;
    padding: 2rem;
    min-height: 300px;
}

.hero-panel h1 {
    font-size: 3rem;
    line-height: 1.02;
    margin: 0.4rem 0 1rem;
}

.hero-panel p {
    color: var(--ks-muted);
    font-size: 1.05rem;
    max-width: 42rem;
}

.hero-aside {
    border: 1px solid var(--ks-line);
    background: #0f172a;
    color: white;
    border-radius: 8px;
    padding: 1.4rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 300px;
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    color: var(--ks-muted);
    font-weight: 800;
    text-transform: uppercase;
    font-size: 0.78rem;
}

.brand-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--ks-red) 0 50%, var(--ks-blue) 50% 100%);
    box-shadow: 0 0 0 4px rgba(18, 60, 156, 0.08);
}

.hero-kpi {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin-top: 1.5rem;
}

.kpi-card,
.module-card,
.insight-card {
    border: 1px solid var(--ks-line);
    background: var(--ks-surface);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 7px 20px rgba(15, 23, 42, 0.05);
}

.kpi-card strong {
    display: block;
    color: var(--ks-text);
    font-size: 1.4rem;
}

.kpi-card span,
.module-card p,
.insight-card p {
    color: var(--ks-muted);
    font-size: 0.93rem;
}

.module-card {
    min-height: 178px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}

.module-card h3 {
    margin: 0 0 0.55rem;
    font-size: 1.05rem;
}

.module-tag {
    color: var(--ks-blue);
    font-weight: 800;
    font-size: 0.76rem;
    text-transform: uppercase;
}

.section-label {
    color: var(--ks-muted);
    font-size: 0.78rem;
    font-weight: 800;
    text-transform: uppercase;
    margin: 1.5rem 0 0.45rem;
}

.card {
    padding: 1.15rem;
    border-radius: 8px;
    border: 1px solid var(--ks-line);
    background: var(--ks-surface);
    min-height: 150px;
    box-shadow: 0 7px 20px rgba(15, 23, 42, 0.05);
}

.card h3 {
    margin-top: 0;
}

.card p,
.small-text {
    color: var(--ks-muted);
    font-size: 0.96rem;
}

div[data-testid="stDataFrame"],
div[data-testid="stTable"] {
    border-radius: 8px;
    overflow: hidden;
}

@media (max-width: 820px) {
    .product-hero,
    .hero-kpi {
        grid-template-columns: 1fr;
    }

    .hero-panel h1 {
        font-size: 2.2rem;
    }
}
</style>
        """,
        unsafe_allow_html=True,
    )
