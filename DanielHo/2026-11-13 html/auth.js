document.addEventListener("DOMContentLoaded", () => {
    // Assign variables from the defined ids in login.html
    const loginForm =
        document.getElementById("loginForm");
    const registerForm =
        document.getElementById("registerForm");
    const logoutButton =
        document.getElementById("logoutButton");
    const currentUser =
        document.getElementById("currentUser");

    // Generate a test user
    if (!localStorage.getItem("users")) {
        const defaultUsers = [
            {
                email: "test@example.com",
                password: "Password123!"
            }
        ];
        localStorage.setItem(
            "users",
            JSON.stringify(defaultUsers)
        );
    }

    // ------------------
    // Protect Home Page
    // ------------------
    
    // If the page is index.html, attach logged in user
    // to the top right
    if (
        window.location.pathname.includes("index.html")
    ) {
        const loggedInUser =
            localStorage.getItem("loggedInUser");
        if (!loggedInUser) {
            window.location.href =
                "./login.html";
            return;
        }
        if (currentUser) {
            currentUser.textContent =
                loggedInUser;
        }
    }

    // ------------------
    // Register
    // ------------------
    if (registerForm) {
        registerForm.addEventListener(
            "submit",
            (event) => {
                event.preventDefault();
                const email =
                    document
                        .getElementById("registerEmail")
                        .value
                        .trim();
                const password =
                    document
                        .getElementById("registerPassword")
                        .value;
                const confirmPassword =
                    document
                        .getElementById("confirmPassword")
                        .value;
                const message =
                    document
                        .getElementById("registerMessage");
                const users =
                    JSON.parse(
                        localStorage.getItem("users")
                    ) || [];
                if (
                    users.find(
                        user => user.email === email
                    )
                ) {
                    message.innerHTML =
                        '<div class="alert alert-danger">User already exists.</div>';

                    return;
                }
                if (
                    password !==
                    confirmPassword
                ) {
                    message.innerHTML =
                        '<div class="alert alert-danger">Passwords do not match.</div>';

                    return;
                }
                users.push({
                    email,
                    password
                });
                localStorage.setItem(
                    "users",
                    JSON.stringify(users)
                );
                message.innerHTML =
                    '<div class="alert alert-success">Registration successful.</div>';
                registerForm.reset();
            }
        );
    }

    // ------------------
    // Login
    // ------------------
    if (loginForm) {
        loginForm.addEventListener(
            "submit",
            (event) => {
                event.preventDefault();
                const email =
                    document
                        .getElementById("loginEmail")
                        .value
                        .trim();
                const password =
                    document
                        .getElementById("loginPassword")
                        .value;
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
                const message =
                    document
                        .getElementById("loginMessage");
                if (!user) {
                    message.innerHTML =
                        '<div class="alert alert-danger">Invalid login.</div>';
                    return;
                }
                localStorage.setItem(
                    "loggedInUser",
                    email
                );
                message.innerHTML =
                    '<div class="alert alert-success">Login successful.</div>';
                setTimeout(() => {
                    window.location.href =
                        "./index.html";
                }, 1000);
            }
        );
    }

    // ------------------
    // Logout
    // ------------------
    if (logoutButton) {
        logoutButton.addEventListener(
            "click",
            () => {
                localStorage.removeItem(
                    "loggedInUser"
                );
                window.location.href =
                    "./login.html";
            }
        );
    }
});