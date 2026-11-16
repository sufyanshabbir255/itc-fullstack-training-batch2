// ---------------------------------------------------------------------------
// 1. Swap two values and return them in the new order.
//    swap(1, 2)  ->  (2, 1)
//    Hint: Python can do this in one line. You saw it in the session.
// ---------------------------------------------------------------------------

function swapString(a, b){
    return [b,a];
};

console.log(swapString(1,2));

// ---------------------------------------------------------------------------
// 2. Return True if n is even, False if it is odd.
//    is_even(4) -> True       is_even(7) -> False
//    Do NOT write `if ...: return True else: return False`. Return the
//    comparison itself — it is already a bool.
// ---------------------------------------------------------------------------

function isEven(n) {
    return n % 2 === 0;
};

console.log(isEven(4));
console.log(isEven(7));
    
// ---------------------------------------------------------------------------
// 3. Convert a number of seconds into minutes and leftover seconds.
//    to_minutes(135) -> (2, 15)
//    Hint: // and %
// ---------------------------------------------------------------------------

function toMinutes(totalSeconds) {
    return [Math.floor(totalSeconds/60), totalSeconds % 60];
};

console.log(toMinutes(135));

// ---------------------------------------------------------------------------
// 4. Build initials from a full name.
//    initials("sufyan shabbir") -> "S.S."
//    initials("ada lovelace")   -> "A.L."
//    Assume exactly two words.
// ---------------------------------------------------------------------------

function initials(fullName) {
    // Split name into parts, ignoring extra spaces
    const parts = fullName.trim().split(/\s+/);

    // Extract first character of each part, uppercase, join with dots
    const result = parts
        .map(part => part.charAt(0).toUpperCase())
        .join('.') + '.';
    return result;
};

console.log(initials("sufyan shabbir"));
console.log(initials("ada lovelace"));

// ---------------------------------------------------------------------------
// 5. Shout a sentence: uppercase, with a single "!" on the end.
//    shout("hello there") -> "HELLO THERE!"
// ---------------------------------------------------------------------------

const shout = text => text.toUpperCase() + '!';

console.log(shout("hello there"));

// ---------------------------------------------------------------------------
// 6. Divide a by b, but return 0 when b is 0 instead of crashing.
//    safe_divide(10, 4) -> 2.5      safe_divide(10, 0) -> 0
//    This is a guard clause: handle the bad case first, then do the real work.
// ---------------------------------------------------------------------------

const safeDivide = (a, b) => {
    if (b === 0) {
        return 0;
    } else {
        return a/b;
    }
};

console.log(safeDivide(10, 4));
console.log(safeDivide(10, 0));

// ---------------------------------------------------------------------------
// 7. Return the average of a list of numbers.
//    average([2, 4, 6]) -> 4.0      average([]) -> 0
//    An empty list must NOT crash.
// ---------------------------------------------------------------------------

const average = (numbers) => {
    if (numbers.length === 0) {
        return 0
    }
    let sum = 0;
    numbers.forEach(num => {
        sum += num;
        }
    );
    return sum / numbers.length;
};

console.log(average([2, 4, 6]));
console.log(average([]));

// ---------------------------------------------------------------------------
// 8. Return the largest number in the list WITHOUT using max().
//    largest([3, 91, 12]) -> 91     largest([-5, -2, -9]) -> -2
//    Careful: seeding your answer with 0 is wrong. Think about why.
// ---------------------------------------------------------------------------

const largest = (numbers) => {
    let bigNumber = numbers[0]
    numbers.forEach(num => {
        if (num > bigNumber) {
            bigNumber = num;
        }
    })
    return bigNumber;
};

console.log(largest([3, 91, 12]));
console.log(largest([-5, -2, -9]));

// ---------------------------------------------------------------------------
// 9. Count how many scores are at or above the pass mark.
//    count_passing([80, 45, 60]) -> 2
//    count_passing([80, 45, 60], 70) -> 1
//    pass_mark has a default of 50.
// ---------------------------------------------------------------------------

function countPassing(scores, passMark=50) {
    let countPasses = 0
    scores.forEach(num => {
        if (num > passMark) {
            countPasses +=1
        };
    });
    return countPasses
};

console.log(countPassing([80, 45, 60]));
console.log(countPassing([80, 45, 60], 70));

// ---------------------------------------------------------------------------
// 10. Reverse the ORDER OF THE WORDS in a sentence (not the letters).
//     reverse_words("python is fun") -> "fun is python"
//     Hint: .split() gives you a list, .join() puts one back together.
// ---------------------------------------------------------------------------

const reverseWords = (sentence) => {
    return sentence
        .trim()
        .split(/\s+/)   // Split into words
        .reverse()      // Reverse word order
        .join(' ');     // Join with single space;
}

console.log(reverseWords("python is fun"));

// ---------------------------------------------------------------------------
// 11. Return the longest word in a sentence.
//     longest_word("I love writing python") -> "writing"
//     If two words tie, return the first one.
// ---------------------------------------------------------------------------
def longest_word(sentence):
    # TODO
    pass

// ---------------------------------------------------------------------------
// 12. Return True if the text reads the same backwards.
//     is_palindrome("racecar") -> True      is_palindrome("python") -> False
//     Ignore capitals: is_palindrome("Level") -> True
// ---------------------------------------------------------------------------
def is_palindrome(text):
    # TODO
    pass

// ---------------------------------------------------------------------------
// 13. FizzBuzz, as a list.
//     For 1..n: multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz",
//     everything else -> the number itself as a string.
//     fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
//     Order your conditions carefully. One of the three must be checked first.
// ---------------------------------------------------------------------------
def fizzbuzz(n):
    # TODO
    pass

// ---------------------------------------------------------------------------
// 14. Running totals.
//     running_total([10, 5, 20]) -> [10, 15, 35]
//     Each entry is the sum of everything up to and including that position.
// ---------------------------------------------------------------------------
def running_total(numbers):
    # TODO
    pass

// ---------------------------------------------------------------------------
// 15. Letter grade for a score.
//     90+ -> "A"   80-89 -> "B"   70-79 -> "C"   60-69 -> "D"   below 60 -> "F"
//     grade_for(85) -> "B"
//     Scores below 0 or above 100 -> "Invalid"
// ---------------------------------------------------------------------------
def grade_for(score):
    # TODO
    pass
