const loginForm = document.getElementById("loginForm");
const formMessage = document.getElementById("formMessage");
const loginButton = document.getElementById("loginButton");

const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

function setMessage(message, type = "") {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type}`.trim();
}

function getApiError(data) {
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg).join(" ");
  }
  return data.detail || "Unable to complete login. Please try again.";
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setMessage("");

  const email = loginForm.email.value.trim().toLowerCase();
  const password = loginForm.password.value;

  if (!email || !password) {
    setMessage("Email and password are required.", "error");
    return;
  }

  if (!emailPattern.test(email)) {
    setMessage("Enter a valid email address.", "error");
    return;
  }

  loginButton.disabled = true;
  loginButton.textContent = "Logging in...";

  try {
    const response = await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(getApiError(data));
    }

    localStorage.setItem(
      "career_session",
      JSON.stringify({
        user: data.user,
        token: data.session_token,
        createdAt: new Date().toISOString(),
      })
    );

    setMessage("Login successful. Redirecting...", "success");
    window.location.href = "/dashboard";
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    loginButton.disabled = false;
    loginButton.textContent = "Login";
  }
});
