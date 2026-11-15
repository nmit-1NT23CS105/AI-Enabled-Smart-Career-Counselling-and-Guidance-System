const registerForm = document.getElementById("registerForm");
const formMessage = document.getElementById("formMessage");
const registerButton = document.getElementById("registerButton");

const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

function setMessage(message, type = "") {
  formMessage.textContent = message;
  formMessage.className = `form-message ${type}`.trim();
}

function isStrongPassword(password) {
  return password.length >= 8 && /[A-Za-z]/.test(password) && /\d/.test(password);
}

function getApiError(data) {
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg).join(" ");
  }
  return data.detail || "Unable to complete registration. Please try again.";
}

registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setMessage("");

  const fullName = registerForm.fullName.value.trim();
  const email = registerForm.email.value.trim().toLowerCase();
  const academicLevel = registerForm.academicLevel.value;
  const password = registerForm.password.value;
  const confirmPassword = registerForm.confirmPassword.value;

  if (!fullName || !email || !academicLevel || !password || !confirmPassword) {
    setMessage("Please complete all required fields.", "error");
    return;
  }

  if (!emailPattern.test(email)) {
    setMessage("Enter a valid email address.", "error");
    return;
  }

  if (!isStrongPassword(password)) {
    setMessage("Password must include at least 8 characters, one letter, and one number.", "error");
    return;
  }

  if (password !== confirmPassword) {
    setMessage("Passwords do not match.", "error");
    return;
  }

  registerButton.disabled = true;
  registerButton.textContent = "Creating account...";

  try {
    const response = await fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        full_name: fullName,
        email,
        password,
        confirm_password: confirmPassword,
        academic_level: academicLevel,
      }),
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

    setMessage("Registration successful. Opening dashboard...", "success");
    window.location.href = "/dashboard";
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    registerButton.disabled = false;
    registerButton.textContent = "Register";
  }
});
