const textInput = document.getElementById("textInput");

const charCount = document.getElementById("charCount");

const analyzeBtn = document.getElementById("analyzeBtn");

const clearBtn = document.getElementById("clearBtn");


/* CHARACTER COUNTER */

textInput.addEventListener("input", () => {

    charCount.textContent =
        `${textInput.value.length} / 5000`;

});


/* CLEAR */

clearBtn.addEventListener("click", () => {

    textInput.value = "";

    charCount.textContent =
        "0 / 5000";

    resetResults();

});


/* ANALYZE */

analyzeBtn.addEventListener(
    "click",
    async () => {

        const text =
            textInput.value.trim();


        if (!text) {

            alert(
                "Please enter some text to analyze."
            );

            return;

        }


        analyzeBtn.disabled = true;

        analyzeBtn.textContent =
            "⏳ Analyzing...";


        try {

            const response =
                await fetch(
                    "/api/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify({
                                text: text
                            })
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "API request failed"
                );

            }


            const data =
                await response.json();


            showResult(data);

            loadDashboard();


        } catch (error) {

            console.error(error);


            document.getElementById(
                "resultTitle"
            ).textContent =
                "Analysis Failed";


            document.getElementById(
                "explanation"
            ).textContent =
                "Unable to connect to the NLPShield backend. Please check that FastAPI is running.";

        }


        finally {

            analyzeBtn.disabled = false;

            analyzeBtn.textContent =
                "🔍 Analyze Text";

        }

    }
);


/* SHOW RESULT */

function showResult(data) {

    const toxicity =
        data.toxicity || {};

    const threat =
        data.threat || {};


    const toxicityConfidence =
        Number(
            toxicity.confidence || 0
        );


    const threatConfidence =
        Number(
            threat.confidence || 0
        );


    const overallConfidence =
        Math.max(
            toxicityConfidence,
            threatConfidence
        );


    const risk =
        String(
            data.risk || "LOW"
        ).toUpperCase();


    /* BASIC RESULT */

    document.getElementById(
        "resultTitle"
    ).textContent =
        "Analysis Complete";


    document.getElementById(
        "toxicityResult"
    ).textContent =
        toxicity.toxic
            ? "TOXIC"
            : "SAFE";


    document.getElementById(
        "threatResult"
    ).textContent =
        threat.threat
            ? "THREAT"
            : "SAFE";


    document.getElementById(
        "confidenceResult"
    ).textContent =
        `${Math.round(
            overallConfidence * 100
        )}%`;


    document.getElementById(
        "categoryResult"
    ).textContent =
        threat.category ||
        "Normal";


    /* EXPLANATION */

    document.getElementById(
        "explanation"
    ).textContent =
        data.explanation ||
        "No explanation available.";


    /* TOXICITY BAR */

    const toxicPercent =
        Math.round(
            toxicityConfidence * 100
        );


    document.getElementById(
        "toxicityConfidence"
    ).textContent =
        `${toxicPercent}%`;


    document.getElementById(
        "toxicityBar"
    ).style.width =
        `${toxicPercent}%`;


    /* THREAT BAR */

    const threatPercent =
        Math.round(
            threatConfidence * 100
        );


    document.getElementById(
        "threatConfidence"
    ).textContent =
        `${threatPercent}%`;


    document.getElementById(
        "threatBar"
    ).style.width =
        `${threatPercent}%`;


    /* RISK */

    const badge =
        document.getElementById(
            "riskBadge"
        );


    badge.textContent =
        risk;


    badge.className =
        `risk-badge ${risk.toLowerCase()}`;


    document.getElementById(
        "riskText"
    ).textContent =
        risk;


    document.getElementById(
        "riskCircle"
    ).textContent =
        risk;


    document.getElementById(
        "riskCircle"
    ).className =
        `risk-circle ${risk.toLowerCase()}`;


    /* RAG */

    showRAGSources(
        data.rag_context || []
    );

}


/* RAG SOURCES */

function showRAGSources(sources) {

    const container =
        document.getElementById(
            "ragSources"
        );


    if (
        !sources ||
        sources.length === 0
    ) {

        container.innerHTML = `
            <p class="muted">
                No relevant security knowledge was retrieved.
            </p>
        `;

        return;

    }


    container.innerHTML =
        sources.map(
            (source) => {

                const name =
                    source.source ||
                    source.file ||
                    "Knowledge Base";


                const score =
                    source.score ?? 0;


                const text =
                    source.text ||
                    "Security guidance retrieved from the knowledge base.";


                return `

                    <div class="rag-item">

                        <div class="rag-top">

                            <strong>
                                📄 ${escapeHtml(name)}
                            </strong>

                            <span>
                                Score: ${score}
                            </span>

                        </div>


                        <p>
                            ${escapeHtml(text)}
                        </p>

                    </div>

                `;

            }
        ).join("");

}


/* DASHBOARD */

async function loadDashboard() {

    try {

        const response =
            await fetch(
                "/api/dashboard"
            );


        if (!response.ok) {
            return;
        }


        const data =
            await response.json();


        document.getElementById(
            "totalAnalyzed"
        ).textContent =
            data.total_analyzed ?? 0;


        document.getElementById(
            "threatsDetected"
        ).textContent =
            data.threats_detected ?? 0;


        document.getElementById(
            "toxicMessages"
        ).textContent =
            data.toxic_messages ?? 0;


        document.getElementById(
            "highRisk"
        ).textContent =
            data.high_risk ?? 0;


    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

    }

}


/* RESET */

function resetResults() {

    document.getElementById(
        "resultTitle"
    ).textContent =
        "Ready to Analyze";


    document.getElementById(
        "toxicityResult"
    ).textContent =
        "—";


    document.getElementById(
        "threatResult"
    ).textContent =
        "—";


    document.getElementById(
        "confidenceResult"
    ).textContent =
        "—";


    document.getElementById(
        "categoryResult"
    ).textContent =
        "—";


    document.getElementById(
        "toxicityConfidence"
    ).textContent =
        "0%";


    document.getElementById(
        "threatConfidence"
    ).textContent =
        "0%";


    document.getElementById(
        "toxicityBar"
    ).style.width =
        "0%";


    document.getElementById(
        "threatBar"
    ).style.width =
        "0%";


    document.getElementById(
        "riskText"
    ).textContent =
        "WAITING";


    document.getElementById(
        "riskCircle"
    ).textContent =
        "—";


    document.getElementById(
        "riskCircle"
    ).className =
        "risk-circle";


    document.getElementById(
        "riskBadge"
    ).textContent =
        "WAITING";


    document.getElementById(
        "riskBadge"
    ).className =
        "risk-badge neutral";


    document.getElementById(
        "explanation"
    ).textContent =
        "Enter text above to receive an AI-powered security analysis.";


    document.getElementById(
        "ragSources"
    ).innerHTML =
        `
        <p class="muted">
            No sources retrieved yet.
        </p>
        `;

}


/* SECURITY */

function escapeHtml(text) {

    const div =
        document.createElement(
            "div"
        );

    div.textContent =
        String(text);

    return div.innerHTML;

}


/* INITIAL LOAD */

loadDashboard();
