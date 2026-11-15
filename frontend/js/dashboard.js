const session = readSession();

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

async function loadRecommendations(userId) {
  const target = document.getElementById("recentRecommendations");

  try {
    const response = await fetch(`/recommendations?user_id=${encodeURIComponent(userId)}`);
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Unable to load recommendations.");
    }

    if (!data.recommendations || data.recommendations.length === 0) {
      target.innerHTML = '<div class="empty-state">No matches yet.</div>';
      return;
    }

    target.innerHTML = data.recommendations
      .slice(0, 3)
      .map(
        (item) => `
          <article class="recent-item">
            <div class="recent-head">
              <span>${escapeHtml(item.career_name)}</span>
              <span class="score-badge">${Number(item.match_score).toFixed(1)}%</span>
            </div>
          </article>
        `
      )
      .join("");
  } catch (error) {
    target.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

const activeSession = requireSession();
if (activeSession) {
  const { user } = activeSession;
  document.getElementById("welcomeTitle").textContent = `Welcome, ${user.full_name}`;
  document.getElementById("dashboardSubtitle").textContent = user.academic_level;
  document.getElementById("topbarName").textContent = user.full_name;
  document.getElementById("avatarInitials").textContent = initials(user.full_name);
  document.getElementById("profileName").textContent = user.full_name;
  document.getElementById("profileEmail").textContent = user.email;
  document.getElementById("profileAcademic").textContent = user.academic_level;
  document.getElementById("logoutButton").addEventListener("click", logout);
  loadRecommendations(user.id);
}
