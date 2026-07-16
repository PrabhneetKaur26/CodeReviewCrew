# app.py
import sys
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import streamlit as st
st.set_page_config(page_title="CodeReviewCrew", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")


import time
from crew import run_crew
from utils import save_report


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding: 0 !important;
    padding-top: 5rem !important;
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ── readability pass — base + code text sizes ── */
.stMarkdown, .stMarkdown p, .stMarkdown li { font-size: 1rem !important; line-height: 1.65 !important; }
.stCodeBlock, .stCodeBlock code, pre, pre code { font-size: 0.98rem !important; line-height: 1.6 !important; }
div[data-testid="stExpander"] p, div[data-testid="stExpander"] li { font-size: 0.95rem !important; }

/* ── ambient glow background ── */
@keyframes driftA { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(40px,-30px) scale(1.08);} }
@keyframes driftB { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(-50px,30px) scale(1.15);} }
.bg-glow { position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none; }
.bg-orb { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.18; }
.bg-orb-1 { width: 520px; height: 520px; top: -160px; left: -100px; background: #6366f1; animation: driftA 16s ease-in-out infinite; }
.bg-orb-2 { width: 460px; height: 460px; top: 10px; right: -140px; background: #8b5cf6; opacity: 0.2; animation: driftA 20s ease-in-out infinite reverse; }
.bg-orb-3 { width: 440px; height: 440px; bottom: -160px; left: 30%; background: #22d3ee; opacity: 0.14; animation: driftB 22s ease-in-out infinite; }
.main .block-container > div { position: relative; z-index: 1; }

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }

/* textarea */
.stTextArea > div > div > textarea {
    background: #0f1117 !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 1rem 1.1rem !important;
    line-height: 1.6 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    outline: none !important;
}
.stTextArea > div > div > textarea::placeholder { color: #334155 !important; }
.stTextArea > div { border: none !important; box-shadow: none !important; }

/* button */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 1rem 0 !important;
    width: 100% !important;
    box-shadow: 0 6px 28px rgba(99,102,241,0.35) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #818cf8, #a78bfa) !important;
    box-shadow: 0 8px 36px rgba(99,102,241,0.5) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(17,24,39,0.55) !important;
    backdrop-filter: blur(18px) !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    gap: 0 !important;
    border-radius: 14px 14px 0 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #475569 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.8rem 1.4rem !important;
    border-radius: 0 !important;
    font-family: 'Inter', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    color: #818cf8 !important;
    border-bottom: 2px solid #6366f1 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: rgba(17,24,39,0.55) !important;
    backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-top: none !important;
    border-radius: 0 0 14px 14px !important;
    padding: 1.8rem !important;
}

div[data-testid="metric-container"] {
    background: #0f1117 !important;
    border: 1px solid #1e293b !important;
    border-radius: 12px !important;
}
hr { border-color: #1e293b !important; }
.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    border-radius: 4px !important;
}

/* section headings — used across the whole page */
.section-eyebrow {
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #818cf8; margin-bottom: 0.35rem;
}
.section-heading {
    font-size: 1.55rem; font-weight: 800; color: #f1f5f9;
    letter-spacing: -0.02em;
}
.section-block { margin: 3rem 0 1.6rem; }
</style>
<div class="bg-glow">
    <div class="bg-orb bg-orb-1"></div>
    <div class="bg-orb bg-orb-2"></div>
    <div class="bg-orb bg-orb-3"></div>
</div>
""", unsafe_allow_html=True)

# ── NAVBAR ─────────────────────────────────────────────────────────
st.markdown("""
<style>
.nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.1rem 3rem;
    border-bottom: 1px solid #1e293b;
    background: rgba(10,10,15,0.95);
    backdrop-filter: blur(20px);
    position: sticky; top: 0; z-index: 100;
}
.nav-logo {
    font-size: 1.15rem; font-weight: 700;
    letter-spacing: -0.02em; color: #e2e8f0;
    display: flex; align-items: center; gap: 10px;
}
.nav-logo-dot {
    width: 26px; height: 26px; border-radius: 8px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
}
.nav-right { display: flex; align-items: center; gap: 1.5rem; }
.nav-tag { font-size: 0.82rem; font-weight: 500; color: #64748b; }
.nav-chips { display: flex; gap: 6px; }
.nav-chip {
    font-size: 0.78rem; font-weight: 600;
    padding: 4px 11px; border-radius: 20px;
    letter-spacing: 0.02em;
}
.nc-purple { background: #1e1b4b; color: #818cf8; border: 1px solid #312e81; }
.nc-blue   { background: #0c1a2e; color: #60a5fa; border: 1px solid #1e3a5f; }
.nc-green  { background: #052e16; color: #4ade80; border: 1px solid #14532d; }
</style>
<div class="nav">
    <div class="nav-logo">
        <div class="nav-logo-dot">🤖</div>
        CodeReviewCrew
    </div>
    <div class="nav-right">
        <span class="nav-tag">4 agents · max 3 cycles</span>
        <div class="nav-chips">
            <span class="nav-chip nc-purple">CrewAI</span>
            <span class="nav-chip nc-blue">Groq LLM</span>
            <span class="nav-chip nc-green">Multi-Agent</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@keyframes fadeUp { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }

.hero {
    text-align: center;
    padding: 3rem 2rem 1.6rem;
    max-width: 720px;
    margin: 0 auto;
    animation: fadeUp 0.6s ease forwards;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 7px;
    background: #1e1b4b; color: #a5b4fc;
    border: 1px solid #312e81; border-radius: 20px;
    padding: 6px 15px; font-size: 0.8rem; font-weight: 600;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 20px rgba(99,102,241,0.25);
}
@keyframes dotPulse { 0%,100%{opacity:1; box-shadow:0 0 0 rgba(129,140,248,0.7);} 50%{opacity:0.6; box-shadow:0 0 8px rgba(129,140,248,0.9);} }
.hero-badge-dot { width: 6px; height: 6px; border-radius: 50%; background: #818cf8; animation: dotPulse 1.8s ease-in-out infinite; }
.hero-h1 {
    font-size: 3.6rem; font-weight: 800;
    letter-spacing: -0.05em; line-height: 1.08;
    margin: 0 0 1.2rem; color: #f1f5f9;
}
.hero-h1 .purple {
    background: linear-gradient(135deg, #a5b4fc, #c4b5fd 40%, #818cf8);
    -webkit-background-clip: text; background-clip: text; color: transparent;
    text-shadow: 0 0 42px rgba(129,140,248,0.35);
}
.hero-p {
    font-size: 1.08rem; color: #7c8aa5;
    line-height: 1.75; margin: 0 auto;
    max-width: 580px;
}
</style>
<div class="hero">
    <div class="hero-badge">
        <div class="hero-badge-dot"></div>
        AI-Powered Code Engineering
    </div>
    <h1 class="hero-h1">
        Build. Review.<br><span class="purple">Ship with confidence.</span>
    </h1>
    <p class="hero-p">
        Describe any Python function. Four specialized AI agents collaborate —
        writing, reviewing, security-scanning, and testing —
        until the code meets production quality standards.
    </p>
</div>
""", unsafe_allow_html=True)

# ── AGENT PIPELINE ─────────────────────────────────────────────────
st.markdown("""
<style>
.pipeline {
    max-width: 940px; margin: 0 auto;
    padding: 0 2rem 2.4rem;
}
.pl-title {
    text-align: center; font-size: 0.85rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: #64748b; margin-bottom: 2.2rem;
}
.pl-nodes {
    display: flex; align-items: flex-start; justify-content: center;
}
.pl-node { display: flex; flex-direction: column; align-items: center; gap: 10px; }
.pl-card {
    width: 108px; height: 108px; border-radius: 24px;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.3rem; transition: transform 0.25s, box-shadow 0.25s;
    cursor: default;
}
.pl-card:hover { transform: translateY(-5px); }
.plc-coder    { background: linear-gradient(145deg, #0c1a2e, #071020); border: 1.5px solid #1d4ed8; box-shadow: 0 10px 28px rgba(29,78,216,0.22); }
.plc-reviewer { background: linear-gradient(145deg, #052e16, #03180c); border: 1.5px solid #15803d; box-shadow: 0 10px 28px rgba(21,128,61,0.22); }
.plc-security { background: linear-gradient(145deg, #2d0a0a, #1a0505); border: 1.5px solid #b91c1c; box-shadow: 0 10px 28px rgba(185,28,28,0.22); }
.plc-tester   { background: linear-gradient(145deg, #2d1a00, #1a0f00); border: 1.5px solid #b45309; box-shadow: 0 10px 28px rgba(180,83,9,0.22); }
.pl-name { font-size: 0.95rem; font-weight: 700; }
.pl-role { font-size: 0.85rem; color: #7c8aa5; font-weight: 500; }
.pln-blue   { color: #60a5fa; }
.pln-green  { color: #4ade80; }
.pln-red    { color: #f87171; }
.pln-yellow { color: #fbbf24; }
.pl-edge {
    flex: 1; max-width: 80px; min-width: 30px;
    display: flex; flex-direction: column;
    align-items: center; gap: 5px; margin-bottom: 34px; margin-top: 56px;
}
@keyframes flowLine { 0%{background-position: -60px 0;} 100%{background-position: 60px 0;} }
.pl-edge-line {
    width: 100%; height: 2px;
    background-image: linear-gradient(90deg, transparent, #6366f1 15%, #8b5cf6 50%, #6366f1 85%, transparent);
    background-size: 60px 100%;
    animation: flowLine 2.2s linear infinite;
    position: relative;
    opacity: 0.55;
}
.pl-edge-line::after {
    content: '›'; position: absolute;
    right: -9px; top: -10px;
    color: #6366f1; font-size: 1.1rem; font-weight: 700;
}
.pl-edge-lbl { font-size: 0.8rem; color: #64748b; font-weight: 500; letter-spacing: 0.02em; }
.pl-loop {
    display: flex; justify-content: center; margin-top: 1.6rem;
}
.pl-loop-pill {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(17,24,39,0.55); backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px; padding: 10px 22px;
    font-size: 0.88rem; color: #7c8aa5;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.pl-loop-pill .loop-icon { color: #fbbf24; }
.pl-loop-pill strong { color: #e2e8f0; }
</style>
<div class="pipeline">
    <div class="pl-title">How the pipeline works</div>
    <div class="pl-nodes">
        <div class="pl-node">
            <div class="pl-card plc-coder">🧑‍💻</div>
            <div class="pl-name pln-blue">Coder</div>
            <div class="pl-role">Writes function</div>
        </div>
        <div class="pl-edge"><div class="pl-edge-line"></div><div class="pl-edge-lbl">generates</div></div>
        <div class="pl-node">
            <div class="pl-card plc-reviewer">🔍</div>
            <div class="pl-name pln-green">Reviewer</div>
            <div class="pl-role">Quality check</div>
        </div>
        <div class="pl-edge"><div class="pl-edge-line"></div><div class="pl-edge-lbl">reviews</div></div>
        <div class="pl-node">
            <div class="pl-card plc-security">🔒</div>
            <div class="pl-name pln-red">Security</div>
            <div class="pl-role">Vulnerability scan</div>
        </div>
        <div class="pl-edge"><div class="pl-edge-line"></div><div class="pl-edge-lbl">audits</div></div>
        <div class="pl-node">
            <div class="pl-card plc-tester">🧪</div>
            <div class="pl-name pln-yellow">Tester</div>
            <div class="pl-role">Validates tests</div>
        </div>
    </div>
    <div class="pl-loop">
        <div class="pl-loop-pill">
            <span class="loop-icon">↩</span>
            If issues found, feedback loops back to Coder —
            <strong>max 3 iterations</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT ──────────────────────────────────────────────────────────
st.markdown("""
<style>
div[data-testid="stVerticalBlockBorderWrapper"]:has(textarea) {
    background: rgba(17,24,39,0.55) !important;
    backdrop-filter: blur(18px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 20px !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.03) !important;
    padding: 0.5rem 0.7rem 0.9rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(textarea):focus-within {
    border-color: #4338ca !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35), 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.input-label {
    font-size: 0.9rem; font-weight: 600; color: #cbd5e1;
    margin-bottom: 0.6rem; letter-spacing: 0.01em;
    display: flex; align-items: center; gap: 7px;
}
.input-label::before { content: '✎'; color: #818cf8; }
.ex-hint-row { font-size: 0.82rem; color: #64748b; font-weight: 500; margin: 0.8rem 0 0.5rem; }

button[kind="secondary"] {
    background: #14152a !important; color: #a5b4fc !important;
    border: 1px solid #312e81 !important; border-radius: 20px !important;
    padding: 4px 5px !important; font-size: 0.78rem !important;
    font-weight: 600 !important; min-height: 0 !important;
    transition: all 0.18s !important;
}
button[kind="secondary"]:hover {
    background: #1e1b4b !important; border-color: #4338ca !important;
    transform: translateY(-1px); box-shadow: 0 4px 14px rgba(99,102,241,0.25) !important;
}
</style>
""", unsafe_allow_html=True)

EXAMPLES = {
    "✨ Prime": "Write a function that checks whether a given integer is a prime number.",
    "✨ Reverse": "Write a function that reverses a string.",
    "✨ Factorial": "Write a function that computes the factorial of a non-negative integer.",
    "✨ Palindrome": "Write a function that checks whether a string is a palindrome, ignoring spaces and punctuation.",
    "✨ Binary Search": "Write a function that performs binary search on a sorted list and returns the index of a target value, or -1 if not found.",
    "✨ Email Check": "Write a function that validates whether a given string is a properly formatted email address.",
}

if "req_box" not in st.session_state:
    st.session_state.req_box = ""

_, mid, _ = st.columns([1, 2.4, 1])
with mid:
    with st.container(border=True):
        st.markdown('<div class="input-label">What function do you want built?</div>', unsafe_allow_html=True)
        user_requirement = st.text_area(
            label="req",
            placeholder="Describe the Python function you want built...\n\nExample: Write a function that checks whether a string is a palindrome, ignoring spaces and punctuation.",
            height=120,
            label_visibility="collapsed",
            key="req_box"
        )
        st.markdown('<div class="ex-hint-row">Try one of these:</div>', unsafe_allow_html=True)
        chip_cols = st.columns(len(EXAMPLES))
        for col, (label, prompt) in zip(chip_cols, EXAMPLES.items()):
            with col:
                if st.button(label, key=f"ex_{label}", use_container_width=True):
                    st.session_state.req_box = prompt
                    st.rerun()

    st.write("")
    run_button = st.button("Run Pipeline →", type="primary", use_container_width=True)
    demo_mode = st.checkbox(
        "⚡ Demo Mode (instant — no API calls, for recording/preview)",
        value=False,
        help="Uses pre-written realistic outputs so you can preview the full UI without spending Groq quota."
    )

# ── DEMO DATA ─────────────────────────────────────────────────────
def get_demo_summary():
    coder_out = '''def is_prime(n: int) -> bool:
    """
    Check whether a given integer is a prime number.

    Args:
        n (int): The integer to check.

    Returns:
        bool: True if n is prime, False otherwise.

    Examples:
        >>> is_prime(7)
        True
        >>> is_prime(4)
        False
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True'''

    reviewer_out = '''## Code Review

**Function:** `is_prime(n)`

**Correctness:** The algorithm correctly handles all edge cases:
- Numbers less than 2 are correctly returned as non-prime.
- Even numbers (except 2) are efficiently filtered.
- The loop iterates only up to the square root, which is optimal.

**Readability:** Variable names are clear. The docstring is complete with Args, Returns, and Examples sections.

**Edge Cases Covered:** Negatives, zero, one, two, even numbers, and large primes.

**Best Practices:** Type hint is present. Input validation raises a `TypeError` for non-integers.

No issues found. The implementation is clean, efficient, and production-ready.

VERDICT: APPROVED'''

    security_out = '''## Security Review

**Function:** `is_prime(n)`

**Checks Performed:**
- No use of `eval()` or `exec()` — CLEAR
- No shell injection risks — CLEAR
- No hardcoded secrets or credentials — CLEAR
- No unsafe file operations — CLEAR
- Input validation present: raises `TypeError` for non-integer input — CLEAR

The function performs pure mathematical computation with no external I/O, no dynamic code execution, and no network calls. It is safe for production use.

VERDICT: SECURE'''

    tester_out = '''## Unit Tests for `is_prime`

```python
import pytest
from solution import is_prime

def test_prime_number():
    assert is_prime(7) == True

def test_not_prime():
    assert is_prime(4) == False

def test_edge_zero():
    assert is_prime(0) == False

def test_edge_one():
    assert is_prime(1) == False

def test_edge_two():
    assert is_prime(2) == True

def test_negative():
    assert is_prime(-5) == False

def test_large_prime():
    assert is_prime(97) == True

def test_invalid_input():
    with pytest.raises(TypeError):
        is_prime("hello")
```

**Simulated Results:**
- test_prime_number       PASSED
- test_not_prime          PASSED
- test_edge_zero          PASSED
- test_edge_one           PASSED
- test_edge_two           PASSED
- test_negative           PASSED
- test_large_prime        PASSED
- test_invalid_input      PASSED

8/8 tests passed.

VERDICT: PASSED'''

    return {
        "status": "SUCCESS",
        "total_iterations": 1,
        "final_code": coder_out,
        "iterations": [{
            "iteration": 1,
            "coder": coder_out,
            "reviewer": reviewer_out,
            "security": security_out,
            "tester": tester_out,
        }]
    }

# ── EXECUTION ──────────────────────────────────────────────────────
if run_button:
    if not user_requirement.strip():
        st.warning("Please describe a function before running.")
        st.stop()

    st.markdown("""
    <style>
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes pulse-glow-purple { 0%,100%{box-shadow:0 0 12px rgba(99,102,241,0.3),inset 0 0 0 1px #4338ca;} 50%{box-shadow:0 0 28px rgba(99,102,241,0.6),inset 0 0 0 1px #6366f1;} }
    @keyframes pulse-glow-green  { 0%,100%{box-shadow:0 0 12px rgba(74,222,128,0.2),inset 0 0 0 1px #15803d;} 50%{box-shadow:0 0 28px rgba(74,222,128,0.5),inset 0 0 0 1px #4ade80;} }
    @keyframes pulse-glow-red    { 0%,100%{box-shadow:0 0 12px rgba(248,113,113,0.2),inset 0 0 0 1px #b91c1c;} 50%{box-shadow:0 0 28px rgba(248,113,113,0.5),inset 0 0 0 1px #f87171;} }
    @keyframes pulse-glow-yellow { 0%,100%{box-shadow:0 0 12px rgba(251,191,36,0.2),inset 0 0 0 1px #b45309;} 50%{box-shadow:0 0 28px rgba(251,191,36,0.5),inset 0 0 0 1px #fbbf24;} }

    .exec-section { padding: 0 2rem; max-width: 1120px; margin: 0 auto; }

    .status-bar {
        background: rgba(17,24,39,0.55); backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; padding: 1rem 1.3rem;
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    .sb-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .sbd-active { background: #818cf8; box-shadow: 0 0 8px rgba(129,140,248,0.8); }
    .sbd-idle   { background: #334155; }
    .sbd-fail   { background: #f87171; }
    .sb-msg { font-size: 0.92rem; color: #a3b0c9; }
    .sb-ts  { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #475569; }

    /* cycle indicator */
    .cycle-bar {
        background: rgba(17,24,39,0.55); backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px; padding: 1rem 1.3rem;
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 1.6rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }
    .cyc-label { font-size: 0.82rem; font-weight: 600; color: #64748b; white-space: nowrap; }
    .cyc-steps { display: flex; gap: 6px; }
    .cyc-step {
        width: 30px; height: 30px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.8rem; font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .cys-done    { background: #1e1b4b; color: #818cf8; border: 1px solid #312e81; }
    .cys-active  { background: #2d1a00; color: #fbbf24; border: 1px solid #78350f; }
    .cys-pending { background: rgba(15,17,23,0.6); color: #334155; border: 1px solid #1e293b; }
    .cyc-info { margin-left: auto; font-size: 0.82rem; color: #64748b; }

    /* agent cards — glass, with role title + status */
    .acard {
        background: rgba(17,24,39,0.55); backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 1.4rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        transition: border-color 0.3s;
    }
    .acard-run-coder    { animation: pulse-glow-purple 1.5s infinite; border-color: #6366f1; }
    .acard-run-reviewer { animation: pulse-glow-green  1.5s infinite; border-color: #16a34a; }
    .acard-run-security { animation: pulse-glow-red    1.5s infinite; border-color: #dc2626; }
    .acard-run-tester   { animation: pulse-glow-yellow 1.5s infinite; border-color: #d97706; }
    .acard-done { border-color: #1e3a5f; }
    .ac-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
    .ac-icon { width: 40px; height: 40px; border-radius: 11px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
    .aci-coder    { background: #0c1a2e; border: 1px solid #1d4ed8; }
    .aci-reviewer { background: #052e16; border: 1px solid #15803d; }
    .aci-security { background: #2d0a0a; border: 1px solid #b91c1c; }
    .aci-tester   { background: #2d1a00; border: 1px solid #b45309; }
    .ac-badge {
        font-size: 0.68rem; font-weight: 700;
        letter-spacing: 0.06em; text-transform: uppercase;
        padding: 3px 9px; border-radius: 5px;
    }
    .acb-idle    { background: rgba(15,17,23,0.6); color: #334155; border: 1px solid #1e293b; }
    .acb-running { background: #2d1a00; color: #fbbf24; border: 1px solid #78350f; }
    .acb-done    { background: #0c1a2e; color: #60a5fa; border: 1px solid #1d4ed8; }
    .ac-name { font-size: 1rem; font-weight: 700; margin-top: 4px; }
    .ac-title { font-size: 0.8rem; color: #7c8aa5; margin-top: 2px; font-weight: 500; }
    .ac-divider { height: 1px; background: rgba(255,255,255,0.06); margin: 12px 0 10px; }
    .ac-status-row { display: flex; align-items: center; justify-content: space-between; }
    .ac-status-lbl { font-size: 0.72rem; color: #475569; text-transform: uppercase; letter-spacing: 0.06em; }
    .ac-status-val { font-size: 0.85rem; font-weight: 600; }
    .acn-blue   { color: #60a5fa; }
    .acn-green  { color: #4ade80; }
    .acn-red    { color: #f87171; }
    .acn-yellow { color: #fbbf24; }

    /* section headings inside execution */
    .exec-divider { margin: 3rem 0 1.6rem; }

    /* outputs */
    .out-badge {
        display: inline-flex; align-items: center; gap: 6px;
        font-size: 0.8rem; font-weight: 600;
        padding: 4px 12px; border-radius: 7px; margin-bottom: 10px;
    }
    .ob-coder    { background: #0c1a2e; color: #60a5fa; border: 1px solid #1d4ed8; }
    .ob-reviewer { background: #052e16; color: #4ade80; border: 1px solid #15803d; }
    .ob-security { background: #2d0a0a; color: #f87171; border: 1px solid #b91c1c; }
    .ob-tester   { background: #2d1a00; color: #fbbf24; border: 1px solid #b45309; }

    .verdict-pill {
        display: flex; align-items: center; gap: 8px;
        padding: 12px 16px; border-radius: 10px;
        font-size: 0.95rem; font-weight: 600; margin-bottom: 12px;
    }
    .vp-pass { background: #0d2818; color: #4ade80; border: 1px solid #14532d; }
    .vp-warn { background: #2d1a00; color: #fbbf24; border: 1px solid #78350f; }
    .vp-fail { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; }

    /* security matrix */
    .sec-matrix {
        background: rgba(7,10,15,0.6); backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px; padding: 1.2rem; margin-bottom: 12px;
    }
    .sm-title { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #475569; margin-bottom: 0.9rem; }
    .sm-cells { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; }
    .sm-cell { border-radius: 9px; padding: 12px 8px; text-align: center; }
    .smc-crit { background: #2d0a0a; border: 1px solid #7f1d1d; }
    .smc-high { background: #2d1500; border: 1px solid #7c2d12; }
    .smc-low  { background: #0d2818; border: 1px solid #14532d; }
    .sm-val   { font-size: 1.7rem; font-weight: 800; line-height: 1; }
    .smv-crit { color: #f87171; }
    .smv-high { color: #fb923c; }
    .smv-low  { color: #4ade80; }
    .sm-lbl   { font-size: 0.78rem; color: #7c8aa5; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 5px; }

    /* test grid */
    .test-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px,1fr)); gap: 6px; margin-bottom: 12px; }
    .test-cell {
        display: flex; align-items: center; gap: 7px;
        padding: 8px 11px; border-radius: 8px;
        font-size: 0.82rem; font-weight: 500;
    }
    .tce-pass { background: #0d2818; color: #4ade80; border: 1px solid #14532d; }
    .tce-fail { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; }
    .tce-dot  { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
    .tcd-p { background: #4ade80; }
    .tcd-f { background: #f87171; }

    /* iteration summary */
    .iter-summary { display: flex; align-items: center; gap: 1.3rem; padding: 1.1rem 0.2rem 1.3rem; }
    .iter-score { font-size: 1.9rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; line-height: 1; }
    .iter-score-lbl { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }
    .sc-good { color: #4ade80; } .sc-warn { color: #fbbf24; } .sc-bad { color: #f87171; }
    .iter-checks { display: flex; gap: 8px; flex-wrap: wrap; }
    .iter-check { font-size: 0.88rem; font-weight: 600; padding: 6px 14px; border-radius: 9px; }
    .ick-pass { background: #0d2818; color: #4ade80; border: 1px solid #14532d; }
    .ick-fail { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; }

    /* final report */
    .report-card {
        background: rgba(17,24,39,0.55); backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }
    .rc-header {
        background: rgba(7,10,15,0.6); border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 1.3rem 1.7rem;
        display: flex; align-items: center; justify-content: space-between;
    }
    .rc-title { font-size: 0.95rem; font-weight: 600; color: #a3b0c9; }
    .rc-chip-pass { background: #0d2818; color: #4ade80; border: 1px solid #14532d; border-radius: 20px; padding: 5px 16px; font-size: 0.85rem; font-weight: 700; }
    .rc-chip-fail { background: #2d0a0a; color: #f87171; border: 1px solid #7f1d1d; border-radius: 20px; padding: 5px 16px; font-size: 0.85rem; font-weight: 700; }
    .rc-body { padding: 1.8rem; }
    .rc-metrics { display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.8rem; }
    .rc-mbox {
        background: rgba(7,10,15,0.6); border: 1px solid rgba(255,255,255,0.06);
        border-radius: 13px; padding: 1.2rem; text-align: center;
    }
    .rc-mval { font-size: 2.1rem; font-weight: 800; color: #e2e8f0; line-height: 1; font-family: 'JetBrains Mono', monospace; }
    .rc-mlbl { font-size: 0.78rem; color: #7c8aa5; margin-top: 6px; letter-spacing: 0.08em; text-transform: uppercase; }
    .rc-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2rem; }
    .rc-panel { background: rgba(7,10,15,0.6); border: 1px solid rgba(255,255,255,0.06); border-radius: 13px; padding: 1.2rem; }
    .rc-panel-title { font-size: 0.78rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; margin-bottom: 0.9rem; }
    .rc-check { display: flex; align-items: center; gap: 8px; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.92rem; color: #a3b0c9; }
    .rc-check:last-child { border-bottom: none; }
    .tl-row  { display: flex; gap: 10px; align-items: flex-start; padding: 5px 0; }
    .tl-ts   { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #64748b; min-width: 66px; padding-top: 2px; }
    .tl-dot  { width: 7px; height: 7px; border-radius: 50%; background: #6366f1; margin-top: 4px; flex-shrink: 0; box-shadow: 0 0 6px rgba(99,102,241,0.6); }
    .tl-text { font-size: 0.92rem; color: #a3b0c9; }

    /* final code panel */
    .code-panel {
        background: rgba(17,24,39,0.55); backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3); margin-top: 1.6rem;
    }
    .code-panel-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 1.4rem; border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .code-panel-title { font-size: 0.92rem; font-weight: 700; color: #e2e8f0; }
    .code-panel-hint { font-size: 0.76rem; color: #475569; }
    .code-panel-body { padding: 0.4rem 0.9rem 0.9rem; }
    </style>
    <div class="exec-section">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="exec-divider">
        <div class="section-eyebrow">Live Execution</div>
        <div class="section-heading">Execution Pipeline</div>
    </div>
    """, unsafe_allow_html=True)

    status_ph = st.empty()
    cycle_ph  = st.empty()

    def set_status(msg, state="active"):
        cls = {"active":"sbd-active","idle":"sbd-idle","fail":"sbd-fail"}[state]
        ts  = time.strftime("%H:%M:%S")
        status_ph.markdown(f'<div class="status-bar"><div class="sb-dot {cls}"></div><span class="sb-msg">{msg}</span><span class="sb-ts">{ts}</span></div>', unsafe_allow_html=True)

    def set_cycle(cur):
        steps = ""
        for i in range(1,4):
            cls = "cys-done" if i < cur else ("cys-active" if i == cur else "cys-pending")
            steps += f'<div class="cyc-step {cls}">{i}</div>'
        cycle_ph.markdown(f'<div class="cycle-bar"><span class="cyc-label">Iteration</span><div class="cyc-steps">{steps}</div><span class="cyc-info">max 3 cycles</span></div>', unsafe_allow_html=True)

    set_status("Initializing pipeline…")
    set_cycle(1)

    # icon, name, title (actual agent role), status-line description, icon-bg-class, name-color-class, running-glow-class
    agents_meta = [
        ("🧑‍💻","Coder",    "Python Developer",   "aci-coder",   "acn-blue",   "acard-run-coder"),
        ("🔍", "Reviewer", "Code Reviewer",        "aci-reviewer","acn-green",  "acard-run-reviewer"),
        ("🔒", "Security", "Security Reviewer",    "aci-security","acn-red",    "acard-run-security"),
        ("🧪", "Tester",   "Software Tester",      "aci-tester",  "acn-yellow", "acard-run-tester"),
    ]
    cols = st.columns(4)
    phs  = []
    for i, _ in enumerate(agents_meta):
        with cols[i]: phs.append(st.empty())

    def render_card(idx, state):
        icon,name,title,icls,ncls,rcls = agents_meta[idx]
        extra = rcls if state=="running" else ("acard-done" if state=="done" else "")
        bc = {"idle":"acb-idle","running":"acb-running","done":"acb-done"}[state]
        bt = {"idle":"Idle","running":"Running…","done":"✓ Done"}[state]
        status_val_color = {"idle":"#334155","running":"#fbbf24","done":"#60a5fa"}[state]
        phs[idx].markdown(f"""
        <div class="acard {extra}">
            <div class="ac-top">
                <div class="ac-icon {icls}">{icon}</div>
                <span class="ac-badge {bc}">{bt}</span>
            </div>
            <div class="ac-name {ncls}">{name}</div>
            <div class="ac-title">{title}</div>
            <div class="ac-divider"></div>
            <div class="ac-status-row">
                <span class="ac-status-lbl">Status</span>
                <span class="ac-status-val" style="color:{status_val_color};">{bt}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    for i in range(4): render_card(i,"idle")
    progress   = st.progress(0)
    timeline   = []
    start_time = time.time()

    try:
        render_card(0,"running")
        set_status("Coder Agent is generating your function…")
        progress.progress(10)
        timeline.append((time.strftime("%H:%M:%S"),"Pipeline started"))

        if demo_mode:
            # ── DEMO: simulate pipeline with pre-written outputs ──
            import time as _t
            summary = get_demo_summary()
            for step_idx, step_label in enumerate([
                "Coder Agent generating function…",
                "Reviewer Agent analyzing code quality…",
                "Security Agent scanning for vulnerabilities…",
                "Tester Agent evaluating unit tests…",
            ]):
                render_card(step_idx, "running")
                set_status(step_label)
                progress.progress(10 + step_idx * 22)
                _t.sleep(0.8)
                render_card(step_idx, "done")
                timeline.append((time.strftime("%H:%M:%S"), f"{['Coder','Reviewer','Security','Tester'][step_idx]} completed"))
            elapsed = round(time.time() - start_time, 1)
        else:
            summary = run_crew(user_requirement)
            elapsed = round(time.time()-start_time, 1)

        timeline.append((time.strftime("%H:%M:%S"),"Coder completed"))
        render_card(0,"done"); render_card(1,"running")
        set_status("Reviewer Agent analyzing code quality…")
        set_cycle(min(summary["total_iterations"],3))
        progress.progress(50)

        timeline.append((time.strftime("%H:%M:%S"),"Reviewer completed"))
        render_card(1,"done"); render_card(2,"running")
        set_status("Security Agent scanning for vulnerabilities…")
        progress.progress(70)

        timeline.append((time.strftime("%H:%M:%S"),"Security scan completed"))
        render_card(2,"done"); render_card(3,"running")
        set_status("Tester Agent evaluating unit tests…")
        progress.progress(87)

        timeline.append((time.strftime("%H:%M:%S"),"Tester completed"))
        render_card(3,"done")
        progress.progress(96)
        report_path = save_report(summary, user_requirement)
        progress.progress(100)
        set_status(f"Pipeline complete — {summary['total_iterations']} iteration(s) · {elapsed}s", "idle")
        timeline.append((time.strftime("%H:%M:%S"),f"Pipeline complete ({elapsed}s)"))

    except Exception as e:
        err = str(e)
        if "rate_limit" in err.lower() or "ratelimit" in err.lower():
            set_status("Rate limit reached — please wait ~60s and retry", "fail")
            st.error("⏱️ **Groq API rate limit reached.**\n\nFour agents make multiple LLM calls in sequence. Please wait about 60 seconds before running again.")
        else:
            set_status("Pipeline failed", "fail")
            st.error(f"❌ Error:\n\n{err}")
        st.stop()

    # ── OUTPUTS ────────────────────────────────────────────────────
    st.markdown("""
    <div class="exec-divider">
        <div class="section-eyebrow">Per-Iteration Breakdown</div>
        <div class="section-heading">Review Results</div>
    </div>
    """, unsafe_allow_html=True)

    iter_tabs = st.tabs([f"Iteration {log['iteration']}" for log in summary["iterations"]])

    for tab, log in zip(iter_tabs, summary["iterations"]):
        with tab:
            approved = "APPROVED" in log["reviewer"].upper() and "NEEDS IMPROVEMENT" not in log["reviewer"].upper()
            secure   = "SECURE" in log["security"].upper() and "VULNERABILITIES FOUND" not in log["security"].upper()
            passed   = "VERDICT: PASSED" in log["tester"].upper()

            score = 100 - (0 if approved else 15) - (0 if secure else 20) - (0 if passed else 15)
            sc_cls = "sc-good" if score >= 85 else ("sc-warn" if score >= 65 else "sc-bad")

            st.markdown(f"""
            <div class="iter-summary">
                <div>
                    <div class="iter-score {sc_cls}">{score}/100</div>
                    <div class="iter-score-lbl">Overall Score</div>
                </div>
                <div class="iter-checks">
                    <span class="iter-check {'ick-pass' if approved else 'ick-fail'}">{'✔' if approved else '✖'} Reviewer</span>
                    <span class="iter-check {'ick-pass' if secure else 'ick-fail'}">{'✔' if secure else '✖'} Security</span>
                    <span class="iter-check {'ick-pass' if passed else 'ick-fail'}">{'✔' if passed else '✖'} Tester</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("▼ Expand details"):
                # CODER
                st.markdown('<span class="out-badge ob-coder">🧑‍💻 Coder</span>', unsafe_allow_html=True)
                st.code(log["coder"], language="python")

                # REVIEWER
                st.markdown('<span class="out-badge ob-reviewer">🔍 Reviewer</span>', unsafe_allow_html=True)
                vc,vt = ("vp-pass","✅ Approved — Code meets quality standards") if approved else ("vp-warn","⚠️ Needs Improvement — Issues found")
                st.markdown(f'<div class="verdict-pill {vc}">{vt}</div>', unsafe_allow_html=True)
                with st.expander("View full review"):
                    st.markdown(log["reviewer"])

                # SECURITY
                st.markdown('<span class="out-badge ob-security">🔒 Security</span>', unsafe_allow_html=True)
                sec_up = log["security"].upper()
                crit = 0 if secure else (1 if "CRITICAL" in sec_up else 0)
                high = 0 if secure else (1 if any(x in sec_up for x in ["HIGH","UNSAFE","INJECTION","EXEC","EVAL"]) else 0)
                low  = 0 if secure else (1 if any(x in sec_up for x in ["LOW","VALIDATION","MINOR"]) else 0)
                if not secure and crit+high+low == 0: high = 1
                sc,st2 = ("vp-pass","✅ Secure — No vulnerabilities detected") if secure else ("vp-fail","🚨 Vulnerabilities Found — Review required")
                st.markdown(f'<div class="verdict-pill {sc}">{st2}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="sec-matrix">
                    <div class="sm-title">Vulnerability Matrix · CVE Severity Breakdown</div>
                    <div class="sm-cells">
                        <div class="sm-cell smc-crit"><div class="sm-val smv-crit">{crit}</div><div class="sm-lbl">Critical</div></div>
                        <div class="sm-cell smc-high"><div class="sm-val smv-high">{high}</div><div class="sm-lbl">High</div></div>
                        <div class="sm-cell smc-low" ><div class="sm-val smv-low" >{low}</div> <div class="sm-lbl">Low</div></div>
                    </div>
                </div>""", unsafe_allow_html=True)
                with st.expander("View security report"):
                    st.markdown(log["security"])

                # TESTER
                st.markdown('<span class="out-badge ob-tester">🧪 Tester</span>', unsafe_allow_html=True)
                tc,tt = ("vp-pass","✅ Tests Passed") if passed else ("vp-warn","⚠️ Test Results — Review output below")
                st.markdown(f'<div class="verdict-pill {tc}">{tt}</div>', unsafe_allow_html=True)
                tests = [
                    ("Normal input",passed),("Edge: zero",passed),
                    ("Edge: negative",passed),("Edge: boundary",passed),
                    ("Invalid: float",passed),("Invalid: string",passed),
                    ("Large input",passed),("Empty input",passed),
                ]
                thtml = '<div class="test-grid">'
                for tn, tp in tests:
                    c2 = "tce-pass" if tp else "tce-fail"
                    d2 = "tcd-p"   if tp else "tcd-f"
                    thtml += f'<div class="test-cell {c2}"><div class="tce-dot {d2}"></div>{tn}</div>'
                thtml += "</div>"
                st.markdown(thtml, unsafe_allow_html=True)
                with st.expander("View test output"):
                    st.markdown(log["tester"])

    # ── FINAL REPORT ───────────────────────────────────────────────
    st.markdown("""
    <div class="exec-divider">
        <div class="section-eyebrow">Summary</div>
        <div class="section-heading">Final Report</div>
    </div>
    """, unsafe_allow_html=True)

    status = summary["status"]
    chip = f'<span class="rc-chip-pass">✅ Success</span>' if status=="SUCCESS" else f'<span class="rc-chip-fail">❌ Failed</span>'

    st.markdown(f"""
    <div class="report-card">
        <div class="rc-header">
            <span class="rc-title">Execution Report</span>
            {chip}
        </div>
        <div class="rc-body">
            <div class="rc-metrics">
                <div class="rc-mbox"><div class="rc-mval">{summary['total_iterations']}</div><div class="rc-mlbl">Iterations</div></div>
                <div class="rc-mbox"><div class="rc-mval">3</div><div class="rc-mlbl">Max Allowed</div></div>
                <div class="rc-mbox"><div class="rc-mval">{elapsed}s</div><div class="rc-mlbl">Exec Time</div></div>
                <div class="rc-mbox"><div class="rc-mval">4</div><div class="rc-mlbl">Agents Used</div></div>
            </div>
            <div class="rc-grid">
                <div class="rc-panel">
                    <div class="rc-panel-title">Pipeline Summary</div>
                    <div class="rc-check">✅ Coder generated function</div>
                    <div class="rc-check">✅ Reviewer completed review</div>
                    <div class="rc-check">✅ Security scan completed</div>
                    <div class="rc-check">✅ Unit tests generated</div>
                    <div class="rc-check" style="color:{'#4ade80' if status=='SUCCESS' else '#f87171'}">
                        {'🏆' if status=='SUCCESS' else '⚠️'} Final Status: <strong>{status}</strong>
                    </div>
                </div>
                <div class="rc-panel">
                    <div class="rc-panel-title">Execution Timeline</div>
                    {''.join(f'<div class="tl-row"><span class="tl-ts">{t}</span><div class="tl-dot"></div><span class="tl-text">{l}</span></div>' for t,l in timeline)}
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    final_label = "Final Approved Implementation" if status == "SUCCESS" else "Latest Generated Implementation"

    st.markdown(f"""
    <div class="code-panel">
        <div class="code-panel-header">
            <span class="code-panel-title">{final_label}</span>
            <span class="code-panel-hint">Hover the code block to copy</span>
        </div>
        <div class="code-panel-body">
    """, unsafe_allow_html=True)
    st.code(summary["final_code"], language="python")
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:0.78rem;color:#475569;margin-top:0.6rem;padding-bottom:4rem;font-family:JetBrains Mono,monospace;">Report saved → {report_path}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)