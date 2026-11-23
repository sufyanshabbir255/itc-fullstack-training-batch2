// ===== [TYPES ON VARIABLES] =====
const appName: string = "TS Basics";
let clickCount: number = 0;
clickCount = clickCount + 1;
console.log("Application name is", appName, "and click count is", clickCount);

// ===== [TYPES ON FUNCTIONS] =====
const square = (n: number): number => n * n;
console.log("3 Squared is", square(3));

// deliberate mistakes that TypeScript catches BEFORE the code runs
// Check with: npx -p typescript tsc --noEmit types.ts

const add = (a: number, b: number): number => a + b;
//console.log("2 + 5 is", add("2", 5));
//fix
console.log("2+5 is", add(2,5));

// ===== [MISTAKE 1] typo in a property name =====
const user = { name: "Hasnaad" };
//console.log(user.nmae);
// tsc: Property 'nmae' does not exist on type '{ name: string; }'
//fix
console.log(user.name);

// ===== [MISTAKE 2] wrong number of inputs =====
const addPart2 = (a: number, b: number): number => a + b;
//addPart2(2);
// tsc: Expected 2 arguments, but got 1
//fix
console.log(addPart2(2,3));

// ===== [MISTAKE 3] reassigning a const =====
//const subject = "JS Basics";
//subject = "Other";
//console.log(subject);
// tsc: Cannot assign to 'subject' because it is a constant
//fix
let subject = "JS Basics";
subject = "Python"
console.log(subject);