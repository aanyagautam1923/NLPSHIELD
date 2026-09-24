import json
import sqlite3
from pathlib import Path
from datetime import datetime

import streamlit as st

from backend.models.toxicity_model import predict_toxicity
from backend.models.threat_model import predict_threat
from backend.rag.knowledge_base import knowledge_base


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "database" / "nlp_shield.db"


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

# Load professional NLPShield UI
UI_CSS = Path(__file__).resolve().parent / "frontend" / "css" / "streamlit.css"

if UI_CSS.exists():
    st.markdown(
        f"<style>{UI_CSS.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )
st.set_page_config(
    page_title="NLPShield",
    page_icon="Shield",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.75;
        margin-bottom: 30px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        background: rgba(128,128,128,0.05);
    }

    .risk-high {
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 0, 0, 0.12);
        border: 1px solid rgba(255, 0, 0, 0.35);
        font-weight: 700;
    }

    .risk-medium {
        padding: 15px;
        border-radius: 10px;
        background: rgba(255, 165, 0, 0.12);
        border: 1px solid rgba(255, 165, 0, 0.35);
        font-weight: 700;
    }

    .risk-low {
        padding: 15px;
        border-radius: 10px;
        background: rgba(0, 180, 80, 0.12);
        border: 1px solid rgba(0, 180, 80, 0.35);
        font-weight: 700;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))


def save_analysis(text, result):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO analyses (text, result_json, created_at)
            VALUES (?, ?, ?)
            """,
            (
                text,
                json.dumps(result),
                datetime.now().isoformat()
            )
        )

        connection.commit()

    finally:
        connection.close()


def get_history(limit=100):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, text, result_json, created_at
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        results = []

        for row in rows:
            try:
                result = json.loads(row[2])
            except Exception:
                result = {}

            results.append(
                {
                    "id": row[0],
                    "text": row[1],
                    "result": result,
                    "created_at": row[3]
                }
            )

        return results

    finally:
        connection.close()


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------

def generate_explanation(toxicity, threat):

    if threat["threat"]:

        category = threat.get("category", "cyber threat")

        explanations = {
            "phishing":
                "The message contains patterns commonly associated with phishing, such as urgent requests, account verification, or suspicious actions.",

            "scam":
                "The message contains patterns commonly associated with scams, including urgency, misleading offers, or suspicious requests.",

            "credential_theft":
                "The message appears to request sensitive credentials such as passwords, account information, or authentication details.",

            "malware":
                "The message contains patterns that may indicate malicious software, suspicious files, or potentially harmful content."
        }

        return explanations.get(
            category,
            "The text contains patterns associated with a potential cyber security threat."
        )

    if toxicity["toxic"]:
        return (
            "The text contains language that the toxicity model "
            "classifies as potentially abusive or toxic."
        )

    return (
        "No strong toxicity or cyber-threat indicators were detected "
        "by the current machine-learning models."
    )


def analyze_text(text):

    toxicity = predict_toxicity(text)
    threat = predict_threat(text)

    if threat["threat"] and threat["confidence"] >= 0.75:
        risk = "HIGH"

    elif threat["threat"] or toxicity["toxic"]:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    rag_results = knowledge_base.search(
        text,
        top_k=5
    )

    explanation = generate_explanation(
        toxicity,
        threat
    )

    result = {
        "toxicity": toxicity,
        "threat": threat,
        "risk": risk,
        "explanation": explanation,
        "rag_context": rag_results
    }

    return result


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("NLPShield")
st.sidebar.caption("AI/NLP Cybersecurity Analyzer")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analyze Text",
        "History",
        "Knowledge Base",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "NLPShield uses machine learning, TF-IDF based retrieval, "
    "RAG and cybersecurity knowledge to analyze text."
)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">NLPShield Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-powered cybersecurity text monitoring</div>',
        unsafe_allow_html=True
    )

    history = get_history(500)

    total = len(history)
    threats = 0
    toxic = 0
    safe = 0
    phishing = 0
    scam = 0
    credential = 0
    malware = 0

    for item in history:

        result = item["result"]

        threat_data = result.get("threat", {})
        toxicity_data = result.get("toxicity", {})

        if threat_data.get("threat"):
            threats += 1
        else:
            safe += 1

        if toxicity_data.get("toxic"):
            toxic += 1

        category = str(
            threat_data.get("category", "")
        ).lower()

        if category == "phishing":
            phishing += 1

        elif category == "scam":
            scam += 1

        elif category == "credential_theft":
            credential += 1

        elif category == "malware":
            malware += 1

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Analyses", total)

    with c2:
        st.metric("Threats Detected", threats)

    with c3:
        st.metric("Toxic Messages", toxic)

    with c4:
        st.metric("Safe Messages", safe)

    st.divider()

    st.subheader("Threat Categories")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Phishing", phishing)

    with c2:
        st.metric("Scams", scam)

    with c3:
        st.metric("Credential Theft", credential)

    with c4:
        st.metric("Malware", malware)

    st.divider()

    st.subheader("Recent Analyses")

    if not history:

        st.info(
            "No analyses yet. Go to Analyze Text and analyze your first message."
        )

    else:

        for item in history[:8]:

            result = item["result"]

            threat_data = result.get("threat", {})
            toxicity_data = result.get("toxicity", {})

            category = threat_data.get(
                "category",
                "normal"
            )

            risk = result.get(
                "risk",
                "LOW"
            )

            st.write(
                f"**#{item['id']}** | "
                f"Risk: **{risk}** | "
                f"Category: **{category}** | "
                f"Toxic: **{toxicity_data.get('toxic', False)}**"
            )

            st.caption(
                item["text"][:180]
            )

            st.divider()


# ---------------------------------------------------------
# ANALYZE PAGE
# ---------------------------------------------------------

elif page == "Analyze Text":

    st.markdown(
        '<div class="main-title">Analyze Text</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Detect toxicity and cybersecurity threats</div>',
        unsafe_allow_html=True
    )

    text = st.text_area(
        "Enter text to analyze",
        height=220,
        placeholder=(
            "Paste an email, message, suspicious text, "
            "or security-related content here..."
        )
    )

    analyze_button = st.button(
        "Analyze Text",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not text.strip():

            st.warning(
                "Please enter some text before analysis."
            )

        else:

            with st.spinner("Analyzing text..."):

                try:

                    result = analyze_text(text)

                    save_analysis(
                        text,
                        result
                    )

                    st.success(
                        "Analysis completed successfully."
                    )

                    st.divider()

                    risk = result["risk"]

                    if risk == "HIGH":
                        st.error("HIGH RISK")

                    elif risk == "MEDIUM":
                        st.warning("MEDIUM RISK")

                    else:
                        st.success("LOW RISK")

                    toxicity = result["toxicity"]
                    threat = result["threat"]

                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.metric(
                            "Toxicity",
                            "Toxic"
                            if toxicity["toxic"]
                            else "Normal"
                        )

                    with c2:
                        st.metric(
                            "Cyber Threat",
                            "Detected"
                            if threat["threat"]
                            else "Safe"
                        )

                    with c3:
                        st.metric(
                            "Threat Category",
                            threat["category"]
                        )

                    with c4:
                        confidence = max(
                            toxicity["confidence"],
                            threat["confidence"]
                        )

                        st.metric(
                            "Confidence",
                            f"{confidence * 100:.2f}%"
                        )

                    st.subheader("AI Explanation")

                    st.write(
                        result["explanation"]
                    )

                    st.subheader("Security Knowledge")

                    rag_context = result["rag_context"]

                    if rag_context:

                        for item in rag_context:

                            with st.expander(
                                item["source"]
                            ):

                                st.write(
                                    item["text"]
                                )

                                st.caption(
                                    f"Retrieval score: {item['score']}"
                                )

                    else:

                        st.info(
                            "No directly matching knowledge-base document was found."
                        )

                    st.subheader("Model Details")

                    st.json(
                        {
                            "toxicity": toxicity,
                            "threat": threat,
                            "risk": risk
                        }
                    )

                except Exception as error:

                    st.error(
                        f"Analysis failed: {error}"
                    )


# ---------------------------------------------------------
# HISTORY
# ---------------------------------------------------------

elif page == "History":

    st.markdown(
        '<div class="main-title">Analysis History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Previously analyzed messages</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "Search history",
        placeholder="Search analyzed text..."
    )

    history = get_history(500)

    if search.strip():

        history = [
            item
            for item in history
            if search.lower()
            in item["text"].lower()
        ]

    if not history:

        st.info(
            "No analysis history found."
        )

    else:

        st.write(
            f"Showing {len(history)} analysis records."
        )

        for item in history:

            result = item["result"]

            threat = result.get(
                "threat",
                {}
            )

            toxicity = result.get(
                "toxicity",
                {}
            )

            with st.expander(
                f"Analysis #{item['id']} - {result.get('risk', 'LOW')}"
            ):

                st.write(
                    "**Text:**",
                    item["text"]
                )

                st.write(
                    "**Threat:**",
                    threat.get("threat")
                )

                st.write(
                    "**Category:**",
                    threat.get("category")
                )

                st.write(
                    "**Toxic:**",
                    toxicity.get("toxic")
                )

                st.write(
                    "**Created:**",
                    item["created_at"]
                )


# ---------------------------------------------------------
# KNOWLEDGE BASE
# ---------------------------------------------------------

elif page == "Knowledge Base":

    st.markdown(
        '<div class="main-title">Knowledge Base</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">RAG cybersecurity knowledge</div>',
        unsafe_allow_html=True
    )

    try:

        if not knowledge_base.loaded:
            count = knowledge_base.load()
        else:
            count = len(
                knowledge_base.documents
            )

        st.metric(
            "Knowledge Documents",
            count
        )

        st.divider()

        documents = knowledge_base.documents

        if not documents:

            st.warning(
                "No knowledge documents found."
            )

        else:

            for index, document in enumerate(
                documents,
                start=1
            ):

                source = document.get(
                    "source",
                    f"Document {index}"
                )

                text = document.get(
                    "text",
                    ""
                )

                with st.expander(
                    source
                ):

                    st.write(text)

    except Exception as error:

        st.error(
            f"Knowledge base error: {error}"
        )


# ---------------------------------------------------------
# ABOUT
# ---------------------------------------------------------

elif page == "About":

    st.markdown(
        '<div class="main-title">About NLPShield</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI/NLP Cyber Threat and Toxicity Analyzer</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        NLPShield is a cybersecurity text analysis platform designed
        to identify potentially harmful, toxic, and suspicious text.
        """
    )

    st.subheader("Technology Stack")

    technologies = [
        "Python",
        "Streamlit",
        "FastAPI",
        "Scikit-learn",
        "TF-IDF",
        "Machine Learning",
        "RAG",
        "SQLite",
        "Ollama / Local LLM"
    ]

    for technology in technologies:
        st.write(f"- {technology}")

    st.subheader("Detection Capabilities")

    capabilities = [
        "Toxicity detection",
        "Phishing detection",
        "Scam detection",
        "Credential theft detection",
        "Malware-related text detection",
        "General cyber-threat detection",
        "RAG-based security information retrieval"
    ]

    for capability in capabilities:
        st.write(f"- {capability}")

    st.divider()

    st.caption(
        "NLPShield - AI/NLP Cybersecurity Project"
    )


