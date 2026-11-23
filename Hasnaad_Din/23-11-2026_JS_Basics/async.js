// ===== [PROMISE] a value that arrives later =====
const orderFood = new Promise(resolve => {
  setTimeout(() => resolve("Pizza is ready"), 2000);
});

console.log("Order placed");
orderFood.then(message => console.log(message));
console.log("Waiting...");

// ===== [ASYNC / AWAIT] same promise, easier to read =====
const eatDinner = async () => {
  console.log("Before await");
  const message = await orderFood;
  console.log("After await:", message);
};

eatDinner();