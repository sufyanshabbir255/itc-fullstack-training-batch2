# ---------------------------------------------------------------------------
# 1. Swap two values and return them in the new order.
#    swap(1, 2)  ->  (2, 1)
#    Hint: Python can do this in one line. You saw it in the session.
# ---------------------------------------------------------------------------
def swap(a, b):
    # TODO
    return b, a

a = 1
b = 2

a,b = swap(a,b)
print (a,b)


# ---------------------------------------------------------------------------
# 2. Return True if n is even, False if it is odd.
#    is_even(4) -> True       is_even(7) -> False
#    Do NOT write `if ...: return True else: return False`. Return the
#    comparison itself — it is already a bool.
# ---------------------------------------------------------------------------
def is_even(n):
    # TODO
    return n % 2 == 0 # % checks if anything is left over
print(is_even(2))
print(is_even(7))
# ---------------------------------------------------------------------------
# 3. Convert a number of seconds into minutes and leftover seconds.
#    to_minutes(135) -> (2, 15)
#    Hint: // and %
# ---------------------------------------------------------------------------
def to_minutes(total_seconds):
    # TODO
    return total_seconds // 60 , total_seconds % 60

print(to_minutes(135))


# ---------------------------------------------------------------------------
# 4. Build initials from a full name.
#    initials("sufyan shabbir") -> "S.S."
#    initials("ada lovelace")   -> "A.L."
#    Assume exactly two words.
# ---------------------------------------------------------------------------
def initials(full_name):
    # TODO
    spilt_words = full_name.split()
    return spilt_words[0][0]+"."+ spilt_words[1][0]+"."
print(initials("Hasnaad Din"))

# ---------------------------------------------------------------------------
# 5. Shout a sentence: uppercase, with a single "!" on the end.
#    shout("hello there") -> "HELLO THERE!"
# ---------------------------------------------------------------------------
def shout(text):
    # TODO
    return text.upper()+'!'
print(shout("hello there"))

# ---------------------------------------------------------------------------
# 6. Divide a by b, but return 0 when b is 0 instead of crashing.
#    safe_divide(10, 4) -> 2.5      safe_divide(10, 0) -> 0
#    This is a guard clause: handle the bad case first, then do the real work.
# ---------------------------------------------------------------------------
def safe_divide(a, b):
    # TODO
    if b == 0:
        answer = 0
    else:
        answer = a/b
    return answer

print(safe_divide(10,0))

# ---------------------------------------------------------------------------
# 7. Return the average of a list of numbers.
#    average([2, 4, 6]) -> 4.0      average([]) -> 0
#    An empty list must NOT crash.
# ---------------------------------------------------------------------------
def average(numbers):
    # TODO
    if len(numbers) == 0:
        averagelist = 0
    else:
        averagelist = sum(numbers) / len(numbers)
    return averagelist
    
print(average([2,4,6]))

# ---------------------------------------------------------------------------
# 8. Return the largest number in the list WITHOUT using max().
#    largest([3, 91, 12]) -> 91     largest([-5, -2, -9]) -> -2
#    Careful: seeding your answer with 0 is wrong. Think about why.
# ---------------------------------------------------------------------------
def largest(numbers):
    largestNum = numbers[0]

    for number in numbers:
        if number > largestNum:
            largestNum = number

    return largestNum

print(largest([-5, -2, -9]))


# ---------------------------------------------------------------------------
# 9. Count how many scores are at or above the pass mark.
#    count_passing([80, 45, 60]) -> 2
#    count_passing([80, 45, 60], 70) -> 1
#    pass_mark has a default of 50.
# ---------------------------------------------------------------------------
def count_passing(scores, pass_mark=50):
    # TODO
    total_score = 0
    for score in scores:
        if score > pass_mark:
            total_score = total_score + 1
    return total_score

print(count_passing([80, 45, 60]))



# ---------------------------------------------------------------------------
# 10. Reverse the ORDER OF THE WORDS in a sentence (not the letters).
#     reverse_words("python is fun") -> "fun is python"
#     Hint: .split() gives you a list, .join() puts one back together.
# ---------------------------------------------------------------------------
def reverse_words(sentence):
    # TODO
    reverse_it = sentence.split()
    reverse_it = reverse_it[::-1]
    return reverse_it

print(reverse_words("python is fun"))

# ---------------------------------------------------------------------------
# 11. Return the longest word in a sentence.
#     longest_word("I love writing python") -> "writing"
#     If two words tie, return the first one.
# ---------------------------------------------------------------------------
def longest_word(sentence):
    # TODO
    words = sentence.split()
    longest = words[0]

    for word in words:
        if word > longest:
            longest = word 
    return longest

print(longest_word("I love writing python"))

# ---------------------------------------------------------------------------
# 12. Return True if the text reads the same backwards.
#     is_palindrome("racecar") -> True      is_palindrome("python") -> False
#     Ignore capitals: is_palindrome("Level") -> True
# ---------------------------------------------------------------------------
def is_palindrome(text):
    # TODO
    text = text.lower()
    backwards = text[::-1]
    if backwards == text:
        is_backwards = True
    else:
        is_backwards = False
    return is_backwards

print(is_palindrome("Level"))


# ---------------------------------------------------------------------------
# 13. FizzBuzz, as a list.
#     For 1..n: multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz",
#     everything else -> the number itself as a string.
#     fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
#     Order your conditions carefully. One of the three must be checked first.
# ---------------------------------------------------------------------------
def fizzbuzz(n):
    # TODO
    result = []

    for num in range(1, n + 1):
        if num % 3 == 0 and num % 5 == 0:
            replace = "FizzBuzz"
            result.append(replace)
        elif num % 3 == 0:
            replace = "Fizz"
            result.append(replace)
        elif num % 5 == 0:
            replace = "Buzz"
            result.append(replace)
        else:
            result.append(num)
        pass

    return result
print(fizzbuzz(15))


# ---------------------------------------------------------------------------
# 14. Running totals.
#     running_total([10, 5, 20]) -> [10, 15, 35]
#     Each entry is the sum of everything up to and including that position.
# ---------------------------------------------------------------------------
def running_total(numbers):
    # TODO
    result = []
    total = 0
    for number in numbers:
        total = total + number
        result.append(total)

    return result

print(running_total([10, 5, 20]))



# ---------------------------------------------------------------------------
# 15. Letter grade for a score.
#     90+ -> "A"   80-89 -> "B"   70-79 -> "C"   60-69 -> "D"   below 60 -> "F"
#     grade_for(85) -> "B"
#     Scores below 0 or above 100 -> "Invalid"
# ---------------------------------------------------------------------------
def grade_for(score):
    # TODO
    if score < 0 or score > 100:
        return "Invalid"
    elif score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

print(grade_for(80))
