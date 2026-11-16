// Simmer - Recipe Finder: Google recipe search

// 1. Find the search form and the text box on the page(both are in the css file)
const searchForm = document.querySelector(".search");
const searchInput = document.querySelector(".search input");

// 2. Run this code when the Search button is clicked (or Enter is pressed)
searchForm.addEventListener("submit", function (event) {
  // Stop the browser's normal behaviour (reloading the page)
  event.preventDefault();

  // 3. Get what the user typed, without spaces at the start or end
  const searchText = searchInput.value.trim();

  // If the box is empty, show a message and stop here
  if (searchText === "") {
    alert("Please type an ingredient or a dish first.");
    return;
  }

  // 4. Build the Google address, e.g. chicken -> "chicken recipe"
  const googleUrl = "https://www.google.com/search?q=" + encodeURIComponent(searchText + " recipe");

  // 5. Open it in a new tab
  window.open(googleUrl, "_blank");
});