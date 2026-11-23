console.log("Hello from basics.js");

// ===== [CONST] value never reassigned =====
const appName = "JS Basics";

// ===== [LET] value will change =====
let clickCount = 0;
//const clickCount = 0;
clickCount = clickCount + 1;
console.log("Application name is", appName, "and click count is", clickCount);

// ===== [CONST OBJECT] change inside, not reassign =====
const user = { name: "Hasnaad" };
user.name = "Hasnaad Din";
//user = { name: "Someone" };
console.log("Name is", user.name);

// ===== [NORMAL FUNCTION] =====
function add(a, b) {
  return a + b;
}

// ===== [ARROW FUNCTION] =====
const addArrow = (a, b) => a + b;
const square = n => n * n;

console.log(add(2, 5), addArrow(2, 5), square(4));

// ===== [ARRAYS + ARROW FUNCTIONS] =====
const prices = [10, 25, 40];
prices.push(55);
console.log("Prices:", prices);

const doubled = prices.map(p => p * 2);
console.log("Doubled:", doubled);

const expensive = prices.filter(p => p > 30);
console.log("Over 30:", expensive);

