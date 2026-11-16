localStorage.setItem(
    "users",
    JSON.stringify(users)
);

fetch("./data/users.json")
    .then(response => response.json())
    .then(users => {
        console.log(users);
    });

document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    const loginMessage = document.getElementById("loginMessage");
    const registerMessage = document.getElementById("registerMessage");

    const currentUser = document.getElementById("currentUser");
    const logoutButton = document.getElementById("logoutButton");

    // -------------------------
    // Utility Functions
    // -------------------------

    function validateCredentials(email, password) {

        const errors = [];

        const emailPattern =
            /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            errors.push("Valid email address required.");
        }

        if (password.length < 8) {
            errors.push(
                "Password must be at least 8 characters."
            );
        }

        if (!/[A-Z]/.test(password)) {
            errors.push(
                "Password needs an uppercase letter."
            );
        }

        if (!/[a-z]/.test(password)) {
            errors.push(
                "Password needs a lowercase letter."
            );
        }

        if (!/[0-9]/.test(password)) {
            errors.push(
                "Password needs a number."
            );
        }

        if (!/[!@#$%^&*]/.test(password)) {
            errors.push(
                "Password needs a special character."
            );
        }

        return errors;
    }

    function showErrors(container, errors) {

        container.innerHTML = `
            <div class="alert alert-danger">
                <ul class="mb-0">
                    ${errors.map(error =>
                        `<li>${error}</li>`
                    ).join("")}
                </ul>
            </div>
        `;
    }

    function updateCurrentUser() {

        const loggedInUser =
            localStorage.getItem("loggedInUser");

        if (loggedInUser) {

            currentUser.textContent =
                `Logged in as: ${loggedInUser}`;

            logoutButton.classList.remove("d-none");

        } else {

            currentUser.textContent =
                "Not Logged In";

            logoutButton.classList.add("d-none");
        }
    }

    // -------------------------
    // Register
    // -------------------------

    registerForm.addEventListener("submit", (event) => {

        event.preventDefault();

        registerMessage.innerHTML = "";

        const email =
            document.getElementById("registerEmail")
                .value
                .trim();

        const password =
            document.getElementById("registerPassword")
                .value;

        const confirmPassword =
            document.getElementById("confirmPassword")
                .value;

        const errors =
            validateCredentials(
                email,
                password
            );

        if (password !== confirmPassword) {
            errors.push(
                "Passwords do not match."
            );
        }

        const users =
            JSON.parse(
                localStorage.getItem("users")
            ) || [];

        const existingUser =
            users.find(
                user => user.email === email
            );

        if (existingUser) {
            errors.push(
                "User already exists."
            );
        }

        if (errors.length > 0) {
            showErrors(
                registerMessage,
                errors
            );
            return;
        }

        users.push({
            email: email,
            password: password
        });

        localStorage.setItem(
            "users",
            JSON.stringify(users)
        );

        registerMessage.innerHTML = `
            <div class="alert alert-success">
                Registration successful!
            </div>
        `;

        registerForm.reset();

        console.log(
            "Registered:",
            email
        );
    });

    // -------------------------
    // Login
    // -------------------------

    loginForm.addEventListener("submit", (event) => {

        event.preventDefault();

        loginMessage.innerHTML = "";

        const email =
            document.getElementById("loginEmail")
                .value
                .trim();

        const password =
            document.getElementById("loginPassword")
                .value;

        const errors =
            validateCredentials(
                email,
                password
            );

        if (errors.length > 0) {
            showErrors(
                loginMessage,
                errors
            );
            return;
        }

        const users =
            JSON.parse(
                localStorage.getItem("users")
            ) || [];

        const user =
            users.find(
                user =>
                    user.email === email &&
                    user.password === password
            );

        if (!user) {

            loginMessage.innerHTML = `
                <div class="alert alert-danger">
                    Invalid email or password.
                </div>
            `;

            return;
        }

        localStorage.setItem(
            "loggedInUser",
            email
        );

        loginMessage.innerHTML = `
            <div class="alert alert-success">
                Welcome back, ${email}!
            </div>
        `;

        updateCurrentUser();

        loginForm.reset();

        console.log(
            "Logged in:",
            email
        );
    });

    // -------------------------
    // Logout
    // -------------------------

    logoutButton.addEventListener("click", () => {

        localStorage.removeItem(
            "loggedInUser"
        );

        updateCurrentUser();

        loginMessage.innerHTML = `
            <div class="alert alert-info">
                You have been logged out.
            </div>
        `;
    });

    // Initial page load
    updateCurrentUser();

});