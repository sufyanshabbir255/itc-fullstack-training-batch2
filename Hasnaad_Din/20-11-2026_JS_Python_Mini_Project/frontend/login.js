// login.js - normal login and Google login. Both save the token and go to posts.html
const message = document.getElementById("message");

function saveTokenAndGo(token) {
  localStorage.setItem("token", token);  // the browser remembers the token
  window.location.href = "posts.html";
}

// 1. Normal login (username OR email + password)
document.getElementById("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();  // stop the page reloading
  const form = new URLSearchParams();  // /login expects form data, not JSON
  form.append("username", document.getElementById("username").value);
  form.append("password", document.getElementById("password").value);

  const response = await fetch("/api/auth/login", { method: "POST", body: form });
  const data = await response.json();
  if (response.ok) {
    saveTokenAndGo(data.access_token);
  } else {
    message.textContent = data.detail;
  }
});

// 2. Google login: Google calls this function after the user picks an account
async function handleGoogleLogin(googleResponse) {
  const response = await fetch("/api/auth/google", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ credential: googleResponse.credential }),
  });
  const data = await response.json();
  if (response.ok) {
    saveTokenAndGo(data.access_token);
  } else {
    message.textContent = data.detail;
  }
}