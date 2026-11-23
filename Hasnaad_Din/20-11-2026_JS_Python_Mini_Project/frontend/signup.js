// signup.js - sends the new user to /api/auth/signup as JSON
const message = document.getElementById("message");

document.getElementById("signup-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const newUser = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  const response = await fetch("/api/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(newUser),
  });
  const data = await response.json();
  if (response.ok) {
    message.textContent = "Account created. You can log in now.";
  } else {
    message.textContent = JSON.stringify(data.detail);
  }
});