async function loadDashboard() {
    try {
        const response = await fetch("/api/dashboard");

        if (!response.ok) {
            throw new Error("Dashboard API failed");
        }

        const data = await response.json();

        updateStats(data);
        updateThreatBars(data);
    } catch (error) {
        console.error("Dashboard loading error:", error);
    }
}


function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value ?? 0;
    }
}


function updateStats(data) {
    const stats = data.stats || data;

    setText(
        "totalAnalyses",
        stats.total_analyses ?? stats.total ?? 0
    );

    setText(
        "threatCount",
        stats.threats ?? stats.threat_count ?? 0
    );

    setText(
        "toxicCount",
        stats.toxic ?? stats.toxic_count ?? 0
    );

    const total =
        Number(stats.total_analyses ?? stats.total ?? 0);

    const threats =
        Number(stats.threats ?? stats.threat_count ?? 0);

    const toxic =
        Number(stats.toxic ?? stats.toxic_count ?? 0);

    const safe =
        stats.safe ??
        stats.safe_count ??
        Math.max(0, total - threats - toxic);

    setText("safeCount", safe);
}


function updateThreatBars(data) {
    const categories =
        data.categories ||
        data.threat_categories ||
        data.category_counts ||
        {};

    const total =
        Object.values(categories)
            .reduce((sum, value) => sum + Number(value || 0), 0);

    updateBar(
        "phishingCount",
        "phishingBar",
        categories.phishing || 0,
        total
    );

    updateBar(
        "scamCount",
        "scamBar",
        categories.scam || 0,
        total
    );

    updateBar(
        "credentialCount",
        "credentialBar",
        categories.credential_theft ||
        categories.credential ||
        0,
        total
    );

    updateBar(
        "malwareCount",
        "malwareBar",
        categories.malware || 0,
        total
    );
}


function updateBar(countId, barId, count, total) {
    const numericCount = Number(count || 0);

    setText(countId, numericCount);

    const bar = document.getElementById(barId);

    if (!bar) {
        return;
    }

    const percentage =
        total > 0
            ? Math.min(100, (numericCount / total) * 100)
            : 0;

    bar.style.width = `${percentage}%`;
}


async function loadRecentAnalyses() {
    const container =
        document.getElementById("recentAnalyses");

    if (!container) {
        return;
    }

    try {
        const response =
            await fetch("/api/history?limit=5");

        if (!response.ok) {
            throw new Error("History API failed");
        }

        const data = await response.json();

        const records =
            Array.isArray(data)
                ? data
                : data.history || data.records || [];

        if (!records.length) {
            container.innerHTML =
                '<p class="panel-subtitle">No analyses yet.</p>';
            return;
        }

        container.innerHTML =
            records.map(createRecentItem).join("");

    } catch (error) {
        console.error(
            "Recent analyses error:",
            error
        );

        container.innerHTML =
            '<p class="panel-subtitle">Unable to load recent analyses.</p>';
    }
}


function createRecentItem(record) {
    let result = record.result;

    if (!result && record.result_json) {
        try {
            result = JSON.parse(record.result_json);
        } catch {
            result = {};
        }
    }

    result = result || {};

    const risk =
        String(result.risk || "LOW").toUpperCase();

    const riskClass =
        risk.toLowerCase();

    const text =
        String(record.text || result.text || "Unknown text");

    const createdAt =
        record.created_at ||
        record.createdAt ||
        "";

    const safeText =
        escapeHtml(
            text.length > 80
                ? text.substring(0, 80) + "..."
                : text
        );

    return `
        <div class="recent-item">
            <div class="recent-text">
                <strong>${safeText}</strong>
                <small>${escapeHtml(createdAt)}</small>
            </div>

            <span class="badge badge-${riskClass}">
                ${escapeHtml(risk)}
            </span>
        </div>
    `;
}


function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


document.addEventListener(
    "DOMContentLoaded",
    () => {
        loadDashboard();
        loadRecentAnalyses();
    }
);
