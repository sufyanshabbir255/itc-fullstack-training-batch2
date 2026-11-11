Simmer - Recipe Finder (Front-end JavaScript Demo)
A one-page recipe finder website built with plain HTML, CSS and JavaScript (no frameworks or libraries), based on the "Simmer - Recipe Finder" Figma design.

Built by Hasnaad Din as part of the ITC Full-Stack training, 10-11 November 2026.

What it does
Shows the Simmer home page: top bar with logo and menu, a big heading, a search box and "Popular" category chips.
Search: type an ingredient or a dish (for example chicken) and click Search or press Enter. A new tab opens with Google results for "chicken recipe".
If the search box is empty, a message asks you to type something first.
Files
File	What it contains
index.html	The page content and structure (what is on the page)
style.css	The design rules: colours, fonts, spacing and layout (how it looks)
script.js	The search behaviour (what it does)
README.md	This file
How to run it
No installation is needed.

Download or clone this branch.
Open the project folder.
Double-click index.html. It opens in your web browser (Edge, Chrome or Firefox).
How the JavaScript works
document.querySelector(".search") finds the search form using the same class name as the CSS.
addEventListener("submit", ...) runs the code when the form is sent (clicking Search or pressing Enter).
event.preventDefault() stops the page from reloading.
The typed text is read with .value.trim(), and the word "recipe" is added to it.
encodeURIComponent(...) makes the text safe for a web address, and window.open(..., "_blank") opens Google in a new tab.
Technologies
HTML5
CSS3 (Flexbox for layout)
JavaScript (no libraries)
Google Fonts: Poppins and Inter