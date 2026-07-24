import streamlit as st
import time
import re
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def clean_markdown_links(text: str) -> str:
    """Find markdown links like [anchor](url) and replace spaces in the URL with %20."""
    def replace_link(match):
        anchor = match.group(1)
        url = match.group(2).strip()
        # Replace spaces in the url with %20 to make it a valid markdown URL
        clean_url = url.replace(" ", "%20")
        return f"[{anchor}]({clean_url})"
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

/* ── CSS Variables ── */
:root {
    --bg:            #0F1117;
    --surface:       #171A21;
    --surface-hover: #1E2130;
    --border:        rgba(255,255,255,0.07);
    --border-accent: rgba(94,106,210,0.4);
    --accent:        #5E6AD2;
    --accent-hover:  #7B88E0;
    --text-primary:  #FFFFFF;
    --text-secondary:#A1A1AA;
    --text-muted:    #6B7280;
    --success:       #22C55E;
    --running:       #3B82F6;
    --error:         #EF4444;
    --radius-sm:     8px;
    --radius-md:     12px;
    --radius-lg:     16px;
    --radius-xl:     20px;
    --shadow-sm:     0 1px 3px rgba(0,0,0,0.4);
    --shadow-md:     0 4px 16px rgba(0,0,0,0.4);
    --shadow-lg:     0 8px 32px rgba(0,0,0,0.5);
    --transition:    all 0.2s ease;
}

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary);
}

/* ── App background ── */
.stApp {
    background-color: var(--bg) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3rem 6rem !important;
    max-width: 1200px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ── Top navigation bar ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}
.navbar-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
}
.navbar-brand span {
    color: var(--accent);
}
.navbar-badge {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--accent);
    background: rgba(94,106,210,0.12);
    border: 1px solid rgba(94,106,210,0.25);
    border-radius: 100px;
    padding: 0.15rem 0.65rem;
    letter-spacing: 0.02em;
}

/* ── Brand Hero Welcome ── */
.brand-hero {
    margin-bottom: 2rem;
    padding-top: 1rem;
}
.brand-tag {
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.brand-title {
    font-size: 2.8rem;
    font-weight: 850;
    color: var(--text-primary);
    margin: 0 0 0.8rem;
    letter-spacing: -0.04em;
    line-height: 1.1;
}
.brand-title span {
    color: var(--accent);
}
.brand-subtitle {
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin: 0;
    font-weight: 400;
}

/* ── Container Overrides via :has() ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent;
    border: none;
    padding: 0;
}

/* Input Card Styling */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.input-card-trigger) {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-xl) !important;
    padding: 2.2rem 2.5rem !important;
    box-shadow: var(--shadow-lg) !important;
    transition: var(--transition) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.input-card-trigger):hover {
    border-color: var(--border-accent) !important;
}
.input-card-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.8rem;
}

/* Live Panel Styling */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.live-panel-trigger) {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-left: 3px solid var(--accent) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.2rem 1.5rem !important;
    margin-bottom: 1rem !important;
    box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.live-panel-trigger.done) {
    border-left-color: var(--success) !important;
    background: rgba(34, 197, 94, 0.02) !important;
}

/* Report Card Styling */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.report-card-trigger) {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-xl) !important;
    padding: 2rem 2.5rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: var(--shadow-lg) !important;
}

/* Critic Card Styling */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.critic-card-trigger) {
    background: rgba(34, 197, 94, 0.03) !important;
    border: 1px solid rgba(34, 197, 94, 0.15) !important;
    border-radius: var(--radius-xl) !important;
    padding: 1.8rem 2.2rem !important;
    margin-bottom: 1.5rem !important;
    box-shadow: var(--shadow-md) !important;
}

/* ── Streamlit text input ── */
.stTextInput > div > div > input {
    background: rgba(0, 0, 0, 0.25) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    padding: 0.75rem 1rem !important;
    transition: var(--transition) !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(94,106,210,0.15) !important;
    outline: none !important;
    background: rgba(0, 0, 0, 0.35) !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--text-muted) !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: -0.01em !important;
    text-transform: none !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.7rem 1.5rem !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(94,106,210,0.35) !important;
    transition: var(--transition) !important;
    width: 100%;
}
.stButton > button:hover {
    background: var(--accent-hover) !important;
    box-shadow: 0 4px 16px rgba(94,106,210,0.45) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    transition: var(--transition) !important;
    box-shadow: none !important;
    padding: 0.6rem 1.2rem !important;
    width: auto !important;
}
.stDownloadButton > button:hover {
    background: var(--surface-hover) !important;
    border-color: var(--accent) !important;
}

/* ── Example chips ── */
.chip {
    display: inline-block;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.35rem 0.9rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin: 0.25rem 0.2rem;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    transition: var(--transition);
}
.chip:hover {
    background: var(--surface-hover);
    border-color: var(--accent);
    color: var(--text-primary);
}

/* ── Pipeline section title ── */
.pipeline-section-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Step card ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    position: relative;
    box-shadow: var(--shadow-sm);
    transition: var(--transition);
}
.step-card.active {
    background: rgba(94,106,210,0.06);
    border-color: var(--accent);
    box-shadow: 0 0 0 1px rgba(94,106,210,0.2), var(--shadow-md);
}
.step-card.done {
    background: rgba(34,197,94,0.03);
    border-color: rgba(34,197,94,0.2);
}

.step-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.65rem;
}
.step-header-left {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex: 1;
}
.step-num {
    font-size: 0.68rem;
    font-weight: 650;
    color: var(--text-muted);
    min-width: 1.8rem;
    font-variant-numeric: tabular-nums;
}
.step-card.active .step-num { color: var(--accent); }
.step-card.done .step-num { color: var(--success); }

.step-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}

.step-desc {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
    line-height: 1.5;
    font-weight: 400;
    padding-left: 2.45rem;
}

.step-status {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 0.2rem 0.6rem;
    border-radius: 100px;
}
.status-waiting {
    color: var(--text-muted);
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
}
.status-running {
    color: var(--running);
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.25);
    animation: pulse-badge 1.4s ease-in-out infinite;
}
.status-done {
    color: var(--success);
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.2);
}
@keyframes pulse-badge {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.55; }
}

/* ── Progress bar ── */
.progress-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 4px;
    overflow: hidden;
    margin: 0.75rem 0 0.2rem;
}
.progress-bar {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--accent), var(--running));
    transition: width 0.5s ease;
}

/* ── Result section title ── */
.result-section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    margin: 2rem 0 1rem;
}

/* ── Result card ── */
.result-card {
    background: transparent;
    border: none;
    padding: 0.5rem 0;
}
.result-card-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.result-card-label::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
}
.result-content {
    font-size: 0.88rem;
    line-height: 1.75;
    color: var(--text-secondary);
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
}

/* ── Report & Critic Labels ── */
.report-card-label {
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.report-card-label::before {
    content: '';
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent);
}

.critic-card-label {
    font-size: 0.72rem;
    font-weight: 750;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--success);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.critic-card-label::before {
    content: '';
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--success);
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
    border-right-color: transparent !important;
    width: 1.5rem !important;
    height: 1.5rem !important;
}

/* ── Expander ── */
details {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: none !important;
    padding: 0.2rem 0.5rem !important;
    margin-bottom: 0.75rem !important;
}
details summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0 !important;
    cursor: pointer !important;
    text-transform: none !important;
}

/* ── Alert ── */
.stAlert {
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: var(--radius-md) !important;
    background: rgba(239,68,68,0.06) !important;
}

/* ── Live streaming ── */
.live-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0.5rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.step-live-header {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-secondary);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.4rem 0.8rem;
    margin: 1rem 0 0.5rem;
    display: inline-block;
}
.live-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.done-label { color: var(--success) !important; }
.live-log {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    color: var(--text-muted);
    line-height: 1.7;
    background: rgba(0,0,0,0.25);
    border-radius: 6px;
    padding: 0.5rem 0.7rem;
}
.live-output {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    color: var(--text-secondary);
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
    padding-right: 0.5rem;
}
.cursor {
    display: inline-block;
    color: var(--accent);
    font-weight: 700;
    animation: blink-cursor 0.85s step-end infinite;
}
@keyframes blink-cursor {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
}

/* ── Site footer ── */
.site-footer {
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    border-top: 1px solid var(--border);
    padding-top: 1.5rem;
    margin-top: 3rem;
}
.footer-brand {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}
.footer-note {
    font-size: 0.72rem;
    color: var(--text-muted);
}

/* ── Markdown inside cards ── */
.report-card-trigger ~ div h1, .report-card-trigger ~ div h2, .report-card-trigger ~ div h3,
.critic-card-trigger ~ div h1, .critic-card-trigger ~ div h2, .critic-card-trigger ~ div h3 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    margin-top: 1.4rem !important;
    margin-bottom: 0.6rem !important;
}
.report-card-trigger ~ div p, .critic-card-trigger ~ div p {
    color: var(--text-secondary) !important;
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
}
.report-card-trigger ~ div li, .critic-card-trigger ~ div li {
    color: var(--text-secondary) !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
}
</style>
""", unsafe_allow_html=True)




# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, icon: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● LIVE",  "status-running"),
        "done":    ("✓ DONE",  "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{icon} {title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div class='step-desc'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Navigation bar ──────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); margin-right: 6px; vertical-align: middle;">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
        Research<span>Mind</span>
    </div>
    <div class="navbar-badge">4 AI Agents &middot; Deep Research</div>
</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_gap, col_pipeline = st.columns([5, 0.4, 4])

with col_input:
    r = st.session_state.results
    if not r and not st.session_state.running:
        st.markdown("""
        <div class="brand-hero">
            <div class="brand-tag">DEEP RESEARCH PLATFORM</div>
            <h1 class="brand-title">Research<span>Mind</span></h1>
            <p class="brand-subtitle">An autonomous multi-agent system that runs search, reads articles, drafts, and critiques detailed scientific or industry reports.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="input-card-trigger"></div>', unsafe_allow_html=True)
        st.markdown('<div class="input-card-title">Research Topic</div>', unsafe_allow_html=True)
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            label_visibility="collapsed",
        )
        run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    # Example chips
    st.markdown("""
    <div style="margin-top:0.8rem; margin-bottom:1.5rem;">
        <span style="font-size:0.72rem;color:var(--text-muted);margin-right:0.4rem;">Try →</span>
        <span class="chip">LLM agents 2025</span>
        <span class="chip">CRISPR gene editing</span>
        <span class="chip">Fusion energy progress</span>
        <span class="chip">GPT-5 capabilities</span>
    </div>
    """, unsafe_allow_html=True)

    # Progress indicator if running
    if st.session_state.running:
        n_done = len(st.session_state.results)
        pct = int((n_done / 4) * 100)
        st.markdown(f"""
        <div style="margin-bottom:1rem;">
            <div style="font-family:'Space Mono',monospace;font-size:0.62rem;color:var(--blue);
                        font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;">
                Pipeline Progress · {pct}%
            </div>
            <div class="progress-wrap">
                <div class="progress-bar" style="width:{pct}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_pipeline:
    r = st.session_state.results

    def s(step):
        if not r and not st.session_state.running:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    st.markdown('<div class="pipeline-section-title">Pipeline · 4 Agents</div>', unsafe_allow_html=True)
    step_card("01", "Search Agent",  "🔍", s("search"), "Finds recent, reliable web sources")
    step_card("02", "Reader Agent",  "📄", s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  "✍️", s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  "🧐", s("critic"), "Reviews, scores & gives feedback")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

# ── Helper: run agent with st.status() live updates ──────────────────────────
def _stream_agent(agent, messages: list, label: str) -> str:
    """Run a LangGraph agent and show live tool calls + response inside st.status()."""
    accumulated = ""

    with st.status(label, expanded=True) as status:
        for event in agent.stream({"messages": messages}, stream_mode="updates"):
            for node_name, node_data in event.items():
                msgs = node_data.get("messages", [])
                for msg in msgs:
                    msg_type = getattr(msg, "type", "")
                    content   = getattr(msg, "content", "")

                    # ── Tool invocation log ──
                    if msg_type == "tool":
                        tool_name = getattr(msg, "name", "tool")
                        st.write(f"🔧 **Tool used:** `{tool_name}`")
                        if content:
                            with st.expander(f"Tool output — {tool_name}", expanded=False):
                                st.text(content[:500] + ("…" if len(content) > 500 else ""))

                    # ── AI final reply ──
                    elif msg_type == "ai" and content:
                        accumulated = content
                        st.write("💬 **Agent response:**")
                        st.markdown(content)

        status.update(label=f"✅ {label} — Done", state="complete", expanded=False)

    return accumulated


# ── Helper: stream a chain with st.write_stream() ────────────────────────────
def _stream_chain(chain, inputs: dict, label: str) -> str:
    """Stream a LangChain LCEL chain token-by-token using st.write_stream()."""

    st.markdown(
        f'<div class="live-label" style="margin-bottom:0.4rem;">✍️ {label}…</div>',
        unsafe_allow_html=True
    )

    def _token_gen():
        for chunk in chain.stream(inputs):
            if isinstance(chunk, str):
                yield chunk
            elif hasattr(chunk, "content"):
                yield chunk.content
            else:
                yield str(chunk)

    # st.write_stream() renders tokens live as they arrive — this is the correct Streamlit API
    result = st.write_stream(_token_gen())

    st.markdown(
        f'<div class="live-label" style="color:var(--green);margin-top:0.2rem;">✅ {label} — Complete</div>',
        unsafe_allow_html=True
    )
    return result


if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="live-section-title">🔴 Live Pipeline Output</div>',
        unsafe_allow_html=True
    )

    # ── Step 1: Search ──────────────────────────────────────────────────────
    st.markdown('<div class="step-live-header">01 · 🔍 Search Agent</div>', unsafe_allow_html=True)
    search_agent = build_search_agent()
    search_out = _stream_agent(
        search_agent,
        [("user", f"Find recent, reliable and detailed information about: {topic_val}")],
        label="🔍 Search Agent — Scanning the web"
    )
    results["search"] = search_out
    st.session_state.results = dict(results)

    # ── Step 2: Reader ──────────────────────────────────────────────────────
    st.markdown('<div class="step-live-header">02 · 📄 Reader Agent</div>', unsafe_allow_html=True)
    reader_agent = build_reader_agent()
    reader_out = _stream_agent(
        reader_agent,
        [("user",
            f"Based on the following search results about '{topic_val}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{results['search'][:800]}"
        )],
        label="📄 Reader Agent — Scraping content"
    )
    results["reader"] = reader_out
    st.session_state.results = dict(results)

    # ── Step 3: Writer ──────────────────────────────────────────────────────
    st.markdown('<div class="step-live-header">03 · ✍️ Writer Chain</div>', unsafe_allow_html=True)
    research_combined = (
        f"SEARCH RESULTS:\n{results['search']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
    )

    # Extract URLs from search results
    urls_list = re.findall(r'URL:\s*(https?://[^\s\)]+)', results["search"])
    # Remove duplicates while preserving order
    urls_list = list(dict.fromkeys(urls_list))
    formatted_urls = "\n".join(f"- {url}" for url in urls_list) if urls_list else "No URLs found in research."

    with st.container(border=True):
        st.markdown('<div class="live-panel-trigger"></div>', unsafe_allow_html=True)
        writer_out = _stream_chain(
            writer_chain,
            {"topic": topic_val, "research": research_combined, "urls": formatted_urls},
            label="Drafting Research Report"
        )
    results["writer"] = clean_markdown_links(writer_out)
    st.session_state.results = dict(results)

    # ── Step 4: Critic ──────────────────────────────────────────────────────
    st.markdown('<div class="step-live-header">04 · 🧐 Critic Chain</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="live-panel-trigger"></div>', unsafe_allow_html=True)
        critic_out = _stream_chain(
            critic_chain,
            {"report": results["writer"]},
            label="Reviewing Report"
        )
    results["critic"] = clean_markdown_links(critic_out)
    st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="result-section-title">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍  Search Results (raw output)"):
            st.markdown(
                f'<div class="result-card">'
                f'<div class="result-card-label">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄  Scraped Content (raw output)"):
            st.markdown(
                f'<div class="result-card">'
                f'<div class="result-card-label">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # Final report
    if "writer" in r:
        cleaned_writer = clean_markdown_links(r["writer"])
        with st.container(border=True):
            st.markdown('<div class="report-card-trigger"></div>', unsafe_allow_html=True)
            st.markdown('<div class="report-card-label">📝 Final Research Report</div>', unsafe_allow_html=True)
            st.markdown(cleaned_writer)

        col_dl, col_gap2 = st.columns([3, 7])
        with col_dl:
            st.download_button(
                label="⬇  Download Report (.md)",
                data=cleaned_writer,
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True,
            )

    # Critic feedback
    if "critic" in r:
        cleaned_critic = clean_markdown_links(r["critic"])
        with st.container(border=True):
            st.markdown('<div class="critic-card-trigger"></div>', unsafe_allow_html=True)
            st.markdown('<div class="critic-card-label">🧐 Critic Feedback</div>', unsafe_allow_html=True)
            st.markdown(cleaned_critic)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
    <div class="footer-brand">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent); margin-right: 4px; vertical-align: middle; display: inline-block;">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
        ResearchMind
    </div>
    <div class="footer-note">Powered by LangChain &middot; Multi-Agent Pipeline &middot; Built with Streamlit</div>
</div>
""", unsafe_allow_html=True)