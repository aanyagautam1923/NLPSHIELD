const input = document.getElementById("analyzeInput");
const charCount = document.getElementById("analyzeCharCount");
const clearBtn = document.getElementById("analyzeClearBtn");
const runBtn = document.getElementById("analyzeRunBtn");
const output = document.getElementById("analysisOutput");

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function updateCount() {
    charCount.textContent = `${input.value.length} / 5000`;
}

function setProgress(id, value) {
    const bar = document.getElementById(id);
    if (bar) {
        bar.style.width = `${Math.round(Number(value || 0) * 100)}%`;
    }
}

function formatConfidence(value) {
    return `${Math.round(Number(value || 0) * 100)}%`;
}

function showResult(data) {
    const toxicity = data.toxicity || {};
    const threat = data.threat || {};
    const risk = String(data.risk || "LOW").toUpperCase();

    document.getElementById("analysisTitle").textContent =
        "Analysis Complete";

    const riskBadge = document.getElementById("analysisRiskBadge");
    riskBadge.textContent = risk;
    riskBadge.className = `risk-badge ${risk.toLowerCase()}`;

    document.getElementById("analysisToxicity").textContent =
        toxicity.toxic ? "Toxic" : "Non-Toxic";

    document.getElementById("analysisThreat").textContent =
        threat.threat ? "Threat Detected" : "No Threat";

    document.getElementById("analysisConfidence").textContent =
        formatConfidence(Math.max(
            Number(toxicity.confidence || 0),
            Number(threat.confidence || 0)
        ));

    document.getElementById("analysisCategory").textContent =
        threat.category || "none";

    const toxicityConfidence = Number(toxicity.confidence || 0);
    const threatConfidence = Number(threat.confidence || 0);

    document.getElementById("analysisToxicityConfidence").textContent =
        formatConfidence(toxicityConfidence);

    document.getElementById("analysisThreatConfidence").textContent =
        formatConfidence(threatConfidence);

    setProgress("analysisToxicityBar", toxicityConfidence);
    setProgress("analysisThreatBar", threatConfidence);

    document.getElementById("analysisRisk").textContent = risk;
    document.getElementById("analysisRiskCircle").textContent =
        risk.charAt(0);

    document.getElementById("analysisExplanation").innerHTML =
        `<p>${escapeHtml(
            data.explanation || "No additional explanation available."
        )}</p>`;

    const ragSources = document.getElementById("analysisRagSources");
    const context = Array.isArray(data.rag_context)
        ? data.rag_context
        : [];

    if (context.length === 0) {
        ragSources.innerHTML =
            `<p class="muted">No matching security knowledge found.</p>`;
    } else {
        ragSources.innerHTML = context.map(item => `
            <div class="rag-item">
                <strong>${escapeHtml(item.source || "Knowledge Base")}</strong>
                <p>${escapeHtml(item.text || "")}</p>
            </div>
        `).join("");
    }

    output.hidden = false;
    output.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}

async function analyzeText() {
    const text = input.value.trim();

    if (!text) {
        alert("Please enter some text to analyze.");
        input.focus();
        return;
    }

    if (text.length > 5000) {
        alert("Text cannot exceed 5000 characters.");
        return;
    }

    runBtn.disabled = true;
    runBtn.textContent = "Analyzing...";

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Analysis request failed."
            );
        }

        showResult(data);

    } catch (error) {
        console.error(error);
        alert(`Analysis failed: ${error.message}`);
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = "Analyze Text";
    }
}

function loadExample(text) {
    input.value = text;
    updateCount();
    input.focus();
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

clearBtn.addEventListener("click", () => {
    input.value = "";
    updateCount();
    output.hidden = true;
    input.focus();
});

runBtn.addEventListener("click", analyzeText);

input.addEventListener("input", updateCount);

document.querySelectorAll(".example-card").forEach(card => {
    card.addEventListener("click", () => {
        loadExample(card.dataset.example || "");
    });
});

updateCount();
