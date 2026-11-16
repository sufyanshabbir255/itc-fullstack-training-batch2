const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const showSignup = document.getElementById("showSignup");
const showLogin = document.getElementById("showLogin");
const message = document.getElementById("message");

// 1. Show Signup Form when "Sign Up" is clicked
showSignup.addEventListener("click", function(event) {
    event.preventDefault();
    loginForm.classList.add("hidden");
    signupForm.classList.remove("hidden");
    message.textContent = "";
});

// 2. Show Login Form when "Login" is clicked
showLogin.addEventListener("click", function(event) {
    event.preventDefault();
    signupForm.classList.add("hidden");
    loginForm.classList.remove("hidden");
    message.textContent = "";
});

// 3. Signup Form Submit Handler
signupForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const name = document.getElementById("signupName").value;
    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password.length < 6) {
        message.textContent = "Password must contain at least 6 characters";
        message.style.color = "red";
        return;
    }

    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match";
        message.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/api/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        const data = await response.json();
        message.textContent = data.message;
        message.style.color = data.success ? "green" : "red";

        if (data.success) {
            signupForm.reset();
            signupForm.classList.add("hidden");
            loginForm.classList.remove("hidden");
        }
    } catch (error) {
        message.textContent = "Server error connection failed.";
        message.style.color = "red";
    }
});

// 4. Login Form Submit Handler
loginForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    try {
        const response = await fetch("http://localhost:5000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        message.textContent = data.message;
        message.style.color = data.success ? "green" : "red";

        if (data.success) {
            localStorage.setItem("userName", data.name);
            setTimeout(() => {
                window.location.href = "/home";
            }, 1000);
        }
    } catch (error) {
        message.textContent = "Server error connection failed.";
        message.style.color = "red";
    }
});