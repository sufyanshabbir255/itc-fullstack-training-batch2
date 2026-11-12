// ---------------------------------------------------------------------------
// 1. Swap two values and return them in the new order.
//    swap(1, 2)  ->  (2, 1)
//    Hint: Python can do this in one line. You saw it in the session.
// ---------------------------------------------------------------------------
function swap(a, b){
    return [b, a];
}

let a = 1;
let b = 2;

[a,b] = swap(a,b);
console.log (a,b);

// ---------------------------------------------------------------------------
// 2. Return True if n is even, False if it is odd.
//    is_even(4) -> True       is_even(7) -> False
//    Do NOT write `if ...: return True else: return False`. Return the
//    comparison itself — it is already a bool.
// ---------------------------------------------------------------------------
function is_even(n){
    return n % 2 === 0; // % checks if anything is left over
}

console.log(is_even(2));
console.log(is_even(7));

// ---------------------------------------------------------------------------
// 3. Convert a number of seconds into minutes and leftover seconds.
//    to_minutes(135) -> (2, 15)
//    Hint: // and %
// ---------------------------------------------------------------------------
function to_minutes(total_seconds){
    return [Math.floor(total_seconds / 60), total_seconds % 60];
}

console.log(to_minutes(135));

// ---------------------------------------------------------------------------
// 4. Build initials from a full name.
//    initials("sufyan shabbir") -> "S.S."
//    initials("ada lovelace")   -> "A.L."
//    Assume exactly two words.
// ---------------------------------------------------------------------------
function initials(full_name){
    const spilt_words = full_name.split(" ");
    return spilt_words[0][0]+"."+spilt_words[1][0];
}

console.log(initials("Hasnaad Din"));

// ---------------------------------------------------------------------------
// 5. Shout a sentence: uppercase, with a single "!" on the end.
//    shout("hello there") -> "HELLO THERE!"
// ---------------------------------------------------------------------------
function shout(text){
    return text.toUpperCase()+'!';
}

console.log(shout("hello there"));

// ---------------------------------------------------------------------------
// 6. Divide a by b, but return 0 when b is 0 instead of crashing.
//    safe_divide(10, 4) -> 2.5      safe_divide(10, 0) -> 0
//    This is a guard clause: handle the bad case first, then do the real work.
// ---------------------------------------------------------------------------
function safe_divide(a, b){
    if (b == 0){
        answer = 0;
    }   
    else{
        answer = a/b;
    }

    return answer;
}


console.log(safe_divide(10,0));

// ---------------------------------------------------------------------------
// 7. Return the average of a list of numbers.
//    average([2, 4, 6]) -> 4.0      average([]) -> 0
//    An empty list must NOT crash.
// ---------------------------------------------------------------------------
function average(numbers){
    if (numbers.length === 0){
        return 0;
    }
    let total = 0;
    for (const n of numbers){
        total = total + n;
    }
    return total / numbers.length;
}

console.log(average([2,4,6]));   // 4
console.log(average([]));        // 0

// ---------------------------------------------------------------------------
//  8. Return the largest number in the list WITHOUT using max().
//    largest([3, 91, 12]) -> 91     largest([-5, -2, -9]) -> -2
//    Careful: seeding your answer with 0 is wrong. Think about why.
// ---------------------------------------------------------------------------
function largest(numbers){
    let largestNum = numbers[0];

    for (const number of numbers){
        if( number > largestNum){
            largestNum = number;
        }
            
    }
    return largestNum;
}

console.log(largest([3, 91, 12]));