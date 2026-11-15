const session = readSession();
let chartInstance = null;

function readSession() {
  try {
    return JSON.parse(localStorage.getItem("career_session"));
  } catch {
    return null;
  }
}

function requireSession() {
  if (!session || !session.user) {
    window.location.replace("/login");
    return null;
  }
  return session;
}

function initials(name) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function logout() {
  localStorage.removeItem("career_session");
  localStorage.removeItem("career_results");
  window.location.href = "/login";
}

async function loadResults(userId) {
  const cached = localStorage.getItem("career_results");
  if (cached) {
    try {
      const parsed = JSON.parse(cached);
      if (parsed.user_id === userId && parsed.recommendations) {
        return parsed;
      }
    } catch {
      localStorage.removeItem("career_results");
    }
  }

  const response = await fetch(`/recommendations?user_id=${encodeURIComponent(userId)}`);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || "Unable to load recommendations.");
  }
  return data;
}

function renderList(title, values) {
  const items = Array.isArray(values) ? values : [values];
  if (!items.length || items.every((item) => !item)) {
    return "";
  }

  return `
    <div class="result-list-block">
      <h4>${escapeHtml(title)}</h4>
      <div class="tag-list">
        ${items.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}
      </div>
    </div>
  `;
}

function renderMetrics(metrics = {}) {
  const entries = Object.entries(metrics);
  if (!entries.length) {
    return "";
  }

  return `
    <div class="metric-grid">
      ${entries
        .map(([key, value]) => {
          const renderedValue = Array.isArray(value)
            ? `<div class="tag-list compact">${value.map((item) => `<span>${escapeHtml(item)}</span>`).join("")}</div>`
            : `<strong>${escapeHtml(value)}</strong>`;
          return `
            <div class="metric-tile">
              <span>${escapeHtml(key)}</span>
              ${renderedValue}
            </div>
          `;
        })
        .join("")}
    </div>
  `;
}

function statusClass(value = "") {
  return value.toLowerCase().replaceAll(" ", "-");
}

function renderResults(resultPayload) {
  const list = document.getElementById("resultsList");
  const recommendations = resultPayload.recommendations || [];

  if (resultPayload.academic_level) {
    document.getElementById("resultsSubtitle").textContent = resultPayload.academic_level;
  }

  if (!recommendations.length) {
    list.innerHTML = '<div class="empty-state">No results yet.</div>';
    return;
  }

  list.innerHTML = recommendations
    .map((item, index) => {
      const score = Number(item.match_score);
      const breakdown = item.breakdown || {};
      return `
        <article class="result-card">
          <div class="result-header">
            <div>
              <p class="card-label">Rank ${index + 1}</p>
              <h3>${escapeHtml(item.recommendation_name || item.career_name)}</h3>
              <div class="result-badges">
                <span class="status-pill ${statusClass(item.confidence_label || "Unrated")}">${escapeHtml(item.confidence_label || "Unrated")}</span>
                <span class="status-pill fit">${escapeHtml(item.fit_status || "Fit not rated")}</span>
              </div>
            </div>
            <span class="match-percent">${score.toFixed(1)}%</span>
          </div>
          <div class="progress-track" aria-label="${escapeHtml(item.career_name)} match score">
            <div class="progress-fill" data-score="${score}"></div>
          </div>
          <p><strong>Why:</strong> ${escapeHtml(item.why_recommended)}</p>
          ${renderList("Strengths", item.strengths_detected || [])}
          ${renderList("Gaps", item.missing_areas || [])}
          ${renderList("Fit", item.fit_notes || [])}
          ${renderList("Next", item.suggested_next_steps || [])}
          <div class="breakdown">
            ${Object.entries(breakdown)
              .map(([key, value]) => `<span>${escapeHtml(key)} ${Number(value || 0).toFixed(1)}</span>`)
              .join("")}
          </div>
          ${renderMetrics(item.metrics)}
        </article>
      `;
    })
    .join("");

  requestAnimationFrame(() => {
    document.querySelectorAll(".progress-fill").forEach((bar) => {
      bar.style.width = `${bar.dataset.score}%`;
    });
  });
}

function renderChart(resultPayload) {
  const canvas = document.getElementById("careerChart");
  const recommendations = resultPayload.recommendations || [];
  if (!canvas || !recommendations.length) {
    return;
  }

  if (!window.Chart) {
    canvas.insertAdjacentHTML("afterend", '<div class="empty-state">Chart unavailable.</div>');
    return;
  }

  if (chartInstance) {
    chartInstance.destroy();
  }

  const labels = recommendations.map((item) => item.recommendation_name || item.career_name);
  const scores = recommendations.map((item) => Number(item.match_score));

  chartInstance = new Chart(canvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Match",
          data: scores,
          borderRadius: 8,
          backgroundColor: ["#06B6D4", "#4F46E5", "#7C3AED", "#22C55E", "#F59E0B"],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 900,
        easing: "easeOutQuart",
      },
      plugins: {
        legend: {
          labels: { color: "#FFFFFF" },
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.parsed.y}% match`,
          },
        },
      },
      scales: {
        x: {
          ticks: { color: "#B6C2DC" },
          grid: { color: "rgba(255,255,255,0.08)" },
        },
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { color: "#B6C2DC" },
          grid: { color: "rgba(255,255,255,0.08)" },
        },
      },
    },
  });
}

async function initResults() {
  const activeSession = requireSession();
  if (!activeSession) {
    return;
  }

  document.getElementById("topbarName").textContent = activeSession.user.full_name;
  document.getElementById("avatarInitials").textContent = initials(activeSession.user.full_name);
  document.getElementById("logoutButton").addEventListener("click", logout);

  try {
    const resultPayload = await loadResults(activeSession.user.id);
    renderResults(resultPayload);
    renderChart(resultPayload);
  } catch (error) {
    document.getElementById("resultsList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

initResults();
