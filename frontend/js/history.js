const searchInput = document.getElementById("searchInput");
const historyBody = document.getElementById("historyBody");

let historyData = [];


async function loadHistory() {
    if (!historyBody) {
        return;
    }

    historyBody.innerHTML = `
        <tr>
            <td colspan="8" class="empty">
                Loading analysis history...
            </td>
        </tr>
    `;

    try {
        const response = await fetch("/api/history?limit=100");

        if (!response.ok) {
            throw new Error("History API request failed");
        }

        const data = await response.json();

        historyData = Array.isArray(data)
            ? data
            : data.history || data.records || [];

        renderHistory(historyData);

    } catch (error) {
        console.error("History loading error:", error);

        historyBody.innerHTML = `
            <tr>
                <td colspan="8" class="empty">
                    Unable to load analysis history.
                </td>
            </tr>
        `;
    }
}


function renderHistory(records) {
    if (!historyBody) {
        return;
    }

    if (!records.length) {
        historyBody.innerHTML = `
            <tr>
                <td colspan="8" class="empty">
                    No analysis history found.
                </td>
            </tr>
        `;
        return;
    }

    historyBody.innerHTML = records
        .map(createHistoryRow)
        .join("");
}


function createHistoryRow(record) {
    let result = record.result;

    if (!result && record.result_json) {
        try {
            result = JSON.parse(record.result_json);
        } catch (error) {
            result = {};
        }
    }

    result = result || {};

    const toxicity = result.toxicity || {};
    const threat = result.threat || {};

    const risk = String(
        result.risk || "LOW"
    ).toUpperCase();

    const text = String(
        record.text || result.text || ""
    );

    const category = String(
        threat.category || "normal"
    );

    const createdAt = String(
        record.created_at ||
        record.createdAt ||
        "-"
    );

    const toxicityDetected =
        Boolean(toxicity.toxic);

    const threatDetected =
        Boolean(threat.threat);

    const toxicityClass =
        toxicityDetected ? "danger" : "safe";

    const threatClass =
        threatDetected ? "danger" : "safe";

    const toxicityText =
        toxicityDetected ? "Detected" : "Safe";

    const threatText =
        threatDetected ? "Detected" : "Safe";

    return `
        <tr>
            <td>${escapeHtml(createdAt)}</td>

            <td class="text-cell">
                ${escapeHtml(
                    text.length > 100
                        ? text.substring(0, 100) + "..."
                        : text
                )}
            </td>

            <td>
                <span class="${toxicityClass}">
                    ${toxicityText}
                </span>
            </td>

            <td>
                <span class="${threatClass}">
                    ${threatText}
                </span>
            </td>

            <td>
                ${escapeHtml(category)}
            </td>

            <td>
                ${formatConfidence(toxicity.confidence)}
            </td>

            <td>
                ${formatConfidence(threat.confidence)}
            </td>

            <td>
                <span class="badge ${risk.toLowerCase()}">
                    ${escapeHtml(risk)}
                </span>
            </td>
        </tr>
    `;
}


function formatConfidence(value) {
    const number = Number(value || 0);

    if (!Number.isFinite(number)) {
        return "0%";
    }

    return `${Math.round(number * 100)}%`;
}


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function filterHistory() {
    if (!searchInput) {
        return;
    }

    const query =
        searchInput.value
            .trim()
            .toLowerCase();

    if (!query) {
        renderHistory(historyData);
        return;
    }

    const filtered = historyData.filter(record => {
        let result = record.result;

        if (!result && record.result_json) {
            try {
                result = JSON.parse(record.result_json);
            } catch {
                result = {};
            }
        }

        result = result || {};

        const text =
            String(
                record.text ||
                result.text ||
                ""
            ).toLowerCase();

        const risk =
            String(
                result.risk || ""
            ).toLowerCase();

        const threat =
            String(
                result.threat?.category || ""
            ).toLowerCase();

        return (
            text.includes(query) ||
            risk.includes(query) ||
            threat.includes(query)
        );
    });

    renderHistory(filtered);
}


if (searchInput) {
    searchInput.addEventListener(
        "input",
        filterHistory
    );
}


document.addEventListener(
    "DOMContentLoaded",
    loadHistory
);
