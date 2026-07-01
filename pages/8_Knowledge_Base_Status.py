import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api_client import APIClient
from locales.i18n import get_language, language_selector, t
from ui_style import apply_product_style

st.set_page_config(page_title="知识库状态" if get_language() == "zh" else "Knowledge Base Status", page_icon="🧾", layout="wide")
apply_product_style()
api = APIClient()


def label(en: str, zh: str) -> str:
    return zh if get_language() == "zh" else en


def status_label(value: str) -> str:
    labels = {
        "Official": label("Official", "官方"),
        "Verified": label("Verified", "已验证"),
        "Community": label("Community", "社区"),
        "Mock": label("Mock", "模拟"),
    }
    return labels.get(value, value)


def confidence_label(value: str) -> str:
    labels = {
        "High": label("High", "高"),
        "Medium": label("Medium", "中"),
        "Low": label("Low", "低"),
    }
    return labels.get(value, value)


language_selector("kb_status_language")
if st.button(f"🏠 {t('common.back_home')}"):
    st.switch_page("app.py")

st.markdown(
    f"""
<div class="product-hero">
  <section class="hero-panel">
    <div class="brand-row"><span class="brand-dot"></span>KOREA COMPASS V8</div>
    <h1>{label("Knowledge Base Status", "知识库状态")}</h1>
    <p>{label("Traceability, source coverage, metadata coverage, update cadence, and content confidence for the Korea Compass Knowledge Base.", "查看 Korea Compass 知识库的可追溯性、来源覆盖率、metadata 覆盖率、更新时间和内容可信度。")}</p>
  </section>
  <aside class="hero-aside">
    <h3>{label("Trusted Knowledge Base", "可信知识库")}</h3>
    <p>{label("This admin view helps maintain JSON content quality before future database migration.", "这个管理视图用于维护 JSON 内容质量，并为未来数据库迁移做准备。")}</p>
  </aside>
</div>
""",
    unsafe_allow_html=True,
)

try:
    with st.spinner(t("common.loading_official_data")):
        status = api.get_kb_status()
except Exception as exc:
    st.error(label(f"Knowledge Base status unavailable: {exc}", f"知识库状态暂不可用：{exc}"))
    st.stop()

st.markdown(f"## {label('Knowledge Base Summary', '知识库概览')}")
c1, c2, c3, c4 = st.columns(4)
c1.metric(label("JSON files", "JSON 文件数"), status["total_files"])
c2.metric(label("Valid files", "有效文件"), status["valid_files"])
c3.metric(label("Metadata coverage", "Metadata 覆盖率"), f"{status['metadata_coverage'] * 100:.1f}%")
c4.metric(label("KB version", "知识库版本"), status["knowledge_base_version"])

s1, s2 = st.columns(2)
s1.metric(label("Official coverage", "官方来源覆盖率"), f"{status.get('official_source_coverage', 0) * 100:.1f}%")
s2.metric(label("Mock coverage", "Mock 覆盖率"), f"{status.get('mock_coverage', 0) * 100:.1f}%")

st.markdown(f"## {label('Source Coverage', '来源覆盖率')}")
source_df = pd.DataFrame(
    [{"status": key, "files": value, "ratio": status.get("source_coverage_ratio", {}).get(key, 0)} for key, value in status.get("source_coverage", {}).items()]
)
if not source_df.empty:
    source_df["status_label"] = source_df["status"].map(status_label)
    fig = px.bar(
        source_df,
        x="status_label",
        y="files",
        title=label("Verification status by JSON file", "按 JSON 文件统计的验证状态"),
        labels={"status_label": label("Verification Status", "验证状态"), "files": label("Files", "文件数")},
        color="status_label",
    )
    st.plotly_chart(fig, use_container_width=True)
    source_df["ratio"] = source_df["ratio"].map(lambda value: f"{value * 100:.1f}%")
    st.dataframe(
        source_df[["status_label", "files", "ratio"]].rename(
            columns={"status_label": label("Verification Status", "验证状态"), "files": label("Files", "文件数"), "ratio": label("Ratio", "比例")}
        ),
        use_container_width=True,
        hide_index=True,
    )

st.markdown(f"## {label('Directory Statistics', '目录统计')}")
directory_df = pd.DataFrame(
    [{"directory": key, "files": value} for key, value in status["directory_counts"].items()]
)
if not directory_df.empty:
    fig = px.bar(
        directory_df,
        x="directory",
        y="files",
        title=label("JSON files by directory", "各目录 JSON 文件数"),
        labels={"directory": label("Directory", "目录"), "files": label("Files", "文件数")},
        color="files",
        color_continuous_scale="Blues",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(directory_df, use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.markdown(f"## {label('Update Statistics', '更新时间统计')}")
    update_df = pd.DataFrame(
        [{"last_updated": key, "files": value} for key, value in status["last_updated_counts"].items()]
    )
    if not update_df.empty:
        st.plotly_chart(
            px.pie(update_df, names="last_updated", values="files", title=label("Last updated distribution", "更新时间分布")),
            use_container_width=True,
        )
        st.dataframe(
            update_df.rename(columns={"last_updated": label("Last Updated", "更新时间"), "files": label("Files", "文件数")}),
            use_container_width=True,
            hide_index=True,
        )

with right:
    st.markdown(f"## {label('Confidence Distribution', '可信度分布')}")
    confidence_df = pd.DataFrame(
        [{"confidence": key, "files": value} for key, value in status["confidence_distribution"].items()]
    )
    if not confidence_df.empty:
        confidence_df["confidence_label"] = confidence_df["confidence"].map(confidence_label)
        st.plotly_chart(
            px.pie(confidence_df, names="confidence_label", values="files", title=label("Confidence levels", "可信度等级")),
            use_container_width=True,
        )
        st.dataframe(
            confidence_df[["confidence_label", "files"]].rename(columns={"confidence_label": label("Confidence", "可信度"), "files": label("Files", "文件数")}),
            use_container_width=True,
            hide_index=True,
        )

st.markdown(f"## {label('Validation Issues', '校验问题')}")
issue_cols = st.columns(3)
issues = [
    (label("Missing Metadata", "缺失 Metadata"), status["missing_metadata"]),
    (label("Missing Source", "缺失来源"), status["missing_source"]),
    (label("Missing Last Updated", "缺失更新时间"), status["missing_last_updated"]),
    (label("Missing Official Source", "缺失官方来源"), status.get("missing_official_source", [])),
    (label("Missing Retrieved At", "缺失获取时间"), status.get("missing_retrieved_at", [])),
    (label("Missing Verification Status", "缺失验证状态"), status.get("missing_verification_status", [])),
]
for col, (title, values) in zip(issue_cols * 2, issues):
    with col:
        st.markdown(f"### {title}")
        if values:
            for value in values:
                st.warning(value)
        else:
            st.success(label("No issues", "无问题"))

st.caption(t("common.footer"))
