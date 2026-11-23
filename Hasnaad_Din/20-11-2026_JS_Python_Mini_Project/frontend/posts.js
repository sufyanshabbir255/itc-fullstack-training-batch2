// posts.js - shows who is logged in, lists their posts, saves new posts
const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "index.html";  // not logged in: back to login
}
const authHeader = { Authorization: "Bearer " + token };  // proves who we are to FastAPI

async function loadUser() {
  const response = await fetch("/api/auth/me", { headers: authHeader });
  if (!response.ok) {  // token expired or wrong
    localStorage.removeItem("token");
    window.location.href = "index.html";
    return;
  }
  const user = await response.json();
  document.getElementById("who").textContent = user.username;
}

async function loadPosts() {
  const response = await fetch("/api/posts", { headers: authHeader });
  const posts = await response.json();
  const list = document.getElementById("posts");
  list.innerHTML = "";
  for (const post of posts) {
    const div = document.createElement("div");
    div.className = "post";
    div.innerHTML = "<h3></h3><p></p><small></small>";
    div.querySelector("h3").textContent = post.title;
    div.querySelector("p").textContent = post.content;
    div.querySelector("small").textContent = post.created_at;
    list.appendChild(div);
  }
}

document.getElementById("post-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const newPost = {
    title: document.getElementById("title").value,
    content: document.getElementById("content").value,
  };
  await fetch("/api/posts", {
    method: "POST",
    headers: { ...authHeader, "Content-Type": "application/json" },
    body: JSON.stringify(newPost),
  });
  event.target.reset();  // clear the form
  loadPosts();
});

document.getElementById("logout").addEventListener("click", () => {
  localStorage.removeItem("token");
  window.location.href = "index.html";
});

loadUser();
loadPosts();