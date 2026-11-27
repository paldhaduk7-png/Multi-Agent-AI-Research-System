import time

import streamlit as st

from agents import (
    build_reader_agent,
    build_search_agent,
    invoke_critic,
    invoke_writer,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #1a1d27; border-right: 1px solid #2d3748; }

    /* Cards / info boxes */
    .agent-card {
        background: #1e2130;
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .agent-card h4 { margin: 0 0 4px 0; color: #e2e8f0; font-size: 15px; }
    .agent-card p  { margin: 0; color: #718096; font-size: 13px; }

    /* Status badge */
    .badge-done    { color: #48bb78; font-weight: 600; }
    .badge-running { color: #ed8936; font-weight: 600; }
    .badge-wait    { color: #718096; font-weight: 600; }

    /* Report box */
    .report-box {
        background: #1a1d27;
        border: 1px solid #3182ce;
        border-radius: 12px;
        padding: 24px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1e2130;
        border: 1px solid #2d3748;
        border-radius: 10px;
        padding: 12px 16px;
    }

    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #3182ce, #805ad5);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 28px;
        font-size: 15px;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 Research System")
    st.markdown("---")

    st.markdown("### ⚙️ Pipeline Stages")
    st.markdown("""
    <div class="agent-card">
      <h4>🔍 Search Agent</h4>
      <p>Queries the web via Tavily API and collects the most relevant sources.</p>
    </div>
    <div class="agent-card">
      <h4>🌐 Reader Agent</h4>
      <p>Scrapes top URLs and extracts clean, structured body text.</p>
    </div>
    <div class="agent-card">
      <h4>✍️ Writer Chain</h4>
      <p>Synthesizes all findings into a detailed structured report.</p>
    </div>
    <div class="agent-card">
      <h4>⭐ Critic Chain</h4>
      <p>Evaluates report quality and returns a score with actionable feedback.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧠 Models")
    st.info("Primary: **Google Gemini 2.0 Flash**\nFallback: **Mistral AI**")

    st.markdown("---")
    st.caption("Multi-Agent AI Research System · v1.0")


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🔬 Multi-Agent AI Research System")
st.markdown("Autonomous research powered by **Search → Reader → Writer → Critic** pipeline.")
st.markdown("---")


# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([4, 1])
with col_input:
    topic = st.text_input(
        "Enter Research Topic",
        placeholder="e.g. Impact of war on stock markets",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("🚀 Research")


def _extract(content) -> str:
    """Safely extract plain text from LangChain message content."""
    if isinstance(content, list):
        return "\n".join(
            item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in content
        )
    return str(content)


# ── Pipeline runner ───────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.markdown("---")

    # Live status progress
    status_col, _ = st.columns([3, 1])
    with status_col:
        stage_placeholder = st.empty()

    def show_stage(label: str, done_so_far: list):
        """Render a live pipeline progress indicator."""
        stages = [
            ("🔍 Search Agent",  "Querying Tavily for the latest web sources…"),
            ("🌐 Reader Agent",  "Scraping and extracting page content…"),
            ("✍️ Writer Chain",  "Drafting a structured research report…"),
            ("⭐ Critic Chain",  "Evaluating and scoring the report…"),
        ]
        rows = ""
        for name, desc in stages:
            if name in done_so_far:
                badge = '<span class="badge-done">✔ Done</span>'
            elif name == label:
                badge = '<span class="badge-running">⚡ Running…</span>'
            else:
                badge = '<span class="badge-wait">◌ Waiting</span>'
            rows += f"""
            <div class="agent-card" style="display:flex;justify-content:space-between;align-items:center;">
              <div><h4>{name}</h4><p>{desc}</p></div>
              <div>{badge}</div>
            </div>"""
        stage_placeholder.markdown(rows, unsafe_allow_html=True)

    done: list = []
    state: dict = {}
    t_search = t_read = t_write = t_critic = 0.0

    try:
        # Stage 1 ── Search Agent ─────────────────────────────────────────────
        show_stage("🔍 Search Agent", done)
        t0 = time.time()
        search_agent = build_search_agent()
        res = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = _extract(res["messages"][-1].content)
        done.append("🔍 Search Agent")
        t_search = round(time.time() - t0, 1)

        # Stage 2 ── Reader Agent ─────────────────────────────────────────────
        show_stage("🌐 Reader Agent", done)
        t0 = time.time()
        reader_agent = build_reader_agent()
        res = reader_agent.invoke({
            "messages": [("user",
                f"Based on these search results about '{topic}', pick the most relevant URL "
                f"and scrape it for deeper content.\n\nSearch Results:\n{state['search_results'][:800]}"
            )]
        })
        state["scraped_content"] = _extract(res["messages"][-1].content)
        done.append("🌐 Reader Agent")
        t_read = round(time.time() - t0, 1)

        # Stage 3 ── Writer Chain ─────────────────────────────────────────────
        show_stage("✍️ Writer Chain", done)
        t0 = time.time()
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        # invoke_writer uses _safe_llm_call: auto-fallback to Mistral on quota errors
        state["report"] = invoke_writer(topic, research_combined)
        done.append("✍️ Writer Chain")
        t_write = round(time.time() - t0, 1)

        # Stage 4 ── Critic Chain ─────────────────────────────────────────────
        show_stage("⭐ Critic Chain", done)
        t0 = time.time()
        # invoke_critic uses _safe_llm_call: auto-fallback to Mistral on quota errors
        state["feedback"] = invoke_critic(state["report"])
        done.append("⭐ Critic Chain")
        t_critic = round(time.time() - t0, 1)

        # Mark all done
        show_stage("", done)

    except RuntimeError as e:
        # Friendly quota / fallback error — show orange banner, not red traceback
        stage_placeholder.empty()
        st.warning(f"⚠️ Pipeline stopped early:\n\n{e}")
        st.stop()

    except Exception as e:
        # Unexpected error — show readable message
        stage_placeholder.empty()
        st.error(f"❌ Unexpected error: {type(e).__name__}: {str(e)[:600]}")
        st.stop()

    # ── Metrics row ───────────────────────────────────────────────────────────
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🔍 Search", f"{t_search}s")
    m2.metric("🌐 Scrape", f"{t_read}s")
    m3.metric("✍️ Write", f"{t_write}s")
    m4.metric("⭐ Critique", f"{t_critic}s")

    # ── Report ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📄 Research Report")
    with st.container():
        st.markdown(state["report"])

    # ── Download ──────────────────────────────────────────────────────────────
    st.download_button(
        "📥 Download Report (.md)",
        data=state["report"],
        file_name=f"research_{topic[:40].replace(' ', '_')}.md",
        mime="text/markdown",
    )

    # ── Critic feedback ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## ⭐ Critic Evaluation")
    st.info(state["feedback"])

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic before clicking Research.")
else:
    # ── Default state ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 60px 0; color: #718096;">
      <div style="font-size: 64px;">🔬</div>
      <h3 style="color: #a0aec0;">Enter a research topic above and click <strong>🚀 Research</strong></h3>
      <p>The system will search the web, read top sources, write a full report, and score it – automatically.</p>
    </div>
    """, unsafe_allow_html=True)
