let cartCount = 0;

let cartButtons = document.querySelectorAll(".cart-button");

let cartDisplay = document.querySelector(".cart-count");

cartButtons.forEach(function(button) {

button.addEventListener("click", function() {

cartCount = cartCount + 1;

cartDisplay.textContent = cartCount;

alert("Food added to cart!");

});

});

let categoryButtons = document.querySelectorAll(".category-button");
let foodCards = document.querySelectorAll(".food-card");

categoryButtons.forEach(function(button) {

button.addEventListener("click", function() {

let selectedCategory = button.dataset.category;

foodCards.forEach(function(card) {

if (selectedCategory === "all" ||
selectedCategory === card.dataset.category) {

card.style.display = "block";

} else {

card.style.display = "none";

}

});

});

});