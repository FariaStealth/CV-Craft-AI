import json
import streamlit as st
from cv_parser import extract_text_from_pdf
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Page Config (Centered Single-Page Layout, No Sidebar)
st.set_page_config(
    page_title="CV-Craft AI | Resume Intelligence",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit Default Menu & Sidebar Toggle Completely via CSS
st.markdown("""
    <style>
    /* Hide Streamlit Sidebar & Menu controls */
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Modern Dark Theme Base */
    .stApp {
        background: #030712;
        color: #f9fafb;
    }
    
    /* Hero Header */
    .hero-container {
        text-align: center;
        padding: 30px 20px 10px 20px;
        background: radial-gradient(circle at top, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
        border-radius: 24px;
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 30%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        color: #9ca3af;
        font-size: 16px;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Custom Metric Badges */
    .metric-badge {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .metric-val {
        font-size: 36px;
        font-weight: 800;
        color: #38bdf8;
    }
    .metric-lbl {
        font-size: 12px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* Content Cards */
    .card-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #f3f4f6;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Bullet Point Transformations */
    .diff-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 16px;
    }
    .diff-before {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        padding: 14px;
        border-radius: 12px;
        font-size: 14px;
    }
    .diff-after {
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.2);
        color: #86efac;
        padding: 14px;
        border-radius: 12px;
        font-size: 14px;
    }

    /* Keyword Tags */
    .tag {
        display: inline-block;
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
    }

    /* Clean Container Border for Inputs */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        padding: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cache LLM in RAM for speed
@st.cache_resource
def load_llm():
    return ChatGroq(
        model="llama-3.3-70b-specdec",
        temperature=0.2,
        groq_api_key=st.secrets["GROQ_API_KEY"],
        model_kwargs={"response_format": {"type": "json_object"}}
    )

# 1. HERO HEADER SECTION
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">⚡ CV-Craft AI Studio</div>
        <div class="hero-subtitle">Transform your resume with deep LLM-powered ATS auditing, impact quantification, and precision keyword matching.</div>
    </div>
""", unsafe_allow_html=True)

# 2. MAIN INPUT CONTAINER (Native Clean Container)
with st.container(border=True):
    col_ind, col_role = st.columns(2)
    with col_ind:
        industry = st.selectbox(
            "Target Industry",
            ["IT / Software Engineering", "Business & Management", "Finance & Banking", "Marketing & Growth", "Data & AI"]
        )
    with col_role:
        target_role = st.text_input("Desired Job Title", value="Software Engineer")

    uploaded_file = st.file_uploader("Upload Resume (PDF Format)", type=["pdf"])
    
    st.write("")
    analyze_btn = st.button("✨ Perform Executive Audit", type="primary", use_container_width=True)

# 3. PROCESSING & RESULTS DISPLAY
if analyze_btn:
    if uploaded_file is None:
        st.warning("⚠️ Please select and upload a PDF resume first!")
    else:
        with st.spinner("🔍 Reading document architecture..."):
            cv_text = extract_text_from_pdf(uploaded_file)

        if "Error reading PDF" in cv_text or not cv_text:
            st.error("❌ Unable to extract text from PDF. Ensure it's not a scanned image PDF.")
        else:
            with st.spinner("🤖 Llama 3.2 is auditing profile against industry benchmarks..."):
                llm = load_llm()

                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a senior ATS Auditor and Tech Recruiter. 
                    Perform a strict, high-precision audit of the provided Resume for Industry: {industry} and Target Role: {target_role}.

                    Return response STRICTLY as a valid JSON object matching this schema:
                    {{
                        "overall_score": <number 0-100>,
                        "ats_compatibility_score": <number 0-100>,
                        "keyword_density_score": <number 0-100>,
                        "impact_metrics_score": <number 0-100>,
                        "executive_summary": "A 2-3 sentence overview highlighting candidate positioning.",
                        "critical_mistakes": [
                            "Mistake 1 explanation",
                            "Mistake 2 explanation"
                        ],
                        "missing_keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
                        "improvements": [
                            {{
                                "before": "Original bullet point",
                                "after": "Quantified, high-impact bullet point"
                            }}
                        ]
                    }}
                    """),
                    ("human", "Candidate Resume Content:\n\n{cv_text}")
                ])

                chain = prompt | llm

                try:
                    response = chain.invoke({
                        "industry": industry,
                        "target_role": target_role,
                        "cv_text": cv_text
                    })
                    
                    audit_data = json.loads(response.content)

                    st.markdown("<br><h2 style='text-align: center; color: #f9fafb;'>📊 Audit Insights & Performance</h2><br>", unsafe_allow_html=True)

                    # A. SCORE METRICS (Grid)
                    m1, m2, m3, m4 = st.columns(4)
                    
                    m1.markdown(f"""
                        <div class="metric-badge">
                            <div class="metric-val">{audit_data.get('overall_score', 0)}</div>
                            <div class="metric-lbl">Overall Match</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    m2.markdown(f"""
                        <div class="metric-badge">
                            <div class="metric-val">{audit_data.get('ats_compatibility_score', 0)}%</div>
                            <div class="metric-lbl">ATS Parsability</div>
                        </div>
                    """, unsafe_allow_html=True)

                    m3.markdown(f"""
                        <div class="metric-badge">
                            <div class="metric-val">{audit_data.get('keyword_density_score', 0)}%</div>
                            <div class="metric-lbl">Keywords Density</div>
                        </div>
                    """, unsafe_allow_html=True)

                    m4.markdown(f"""
                        <div class="metric-badge">
                            <div class="metric-val">{audit_data.get('impact_metrics_score', 0)}%</div>
                            <div class="metric-lbl">Impact Score</div>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # B. EXECUTIVE SUMMARY
                    if "executive_summary" in audit_data:
                        st.markdown(f"""
                            <div class="card-box">
                                <div class="card-title">💡 Profile Summary</div>
                                <p style="color: #d1d5db; line-height: 1.6; margin: 0;">{audit_data["executive_summary"]}</p>
                            </div>
                        """, unsafe_allow_html=True)

                    # C. CRITICAL FINDINGS
                    mistakes = audit_data.get("critical_mistakes", [])
                    if mistakes:
                        mistake_list_html = "".join([f"<li style='margin-bottom:8px;'>{m}</li>" for m in mistakes])
                        st.markdown(f"""
                            <div class="card-box" style="border-left: 4px solid #ef4444;">
                                <div class="card-title" style="color: #f87171;">🚨 Critical Areas to Fix</div>
                                <ul style="color: #fca5a5; margin: 0; padding-left: 20px;">
                                    {mistake_list_html}
                                </ul>
                            </div>
                        """, unsafe_allow_html=True)

                    # D. MISSING KEYWORDS
                    keywords = audit_data.get("missing_keywords", [])
                    if keywords:
                        tags_html = "".join([f'<span class="tag">{kw}</span>' for kw in keywords])
                        st.markdown(f"""
                            <div class="card-box">
                                <div class="card-title">🔑 Critical Missing Industry Keywords</div>
                                <div>{tags_html}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    # E. SIDE-BY-SIDE REWRITER
                    improvements = audit_data.get("improvements", [])
                    if improvements:
                        st.markdown("""
                            <div class="card-box">
                                <div class="card-title">✨ Strategic Resume Line Upgrades</div> 
                        """, unsafe_allow_html=True)
                        
                        for item in improvements:
                            st.markdown(f"""
                                <div class="diff-container">
                                    <div class="diff-before">
                                        <strong>Original Line:</strong><br>{item.get('before')}
                                    </div>
                                    <div class="diff-after">
                                        <strong>Upgraded (Impact-Driven):</strong><br>{item.get('after')}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Failed to parse response data: {str(e)}")
