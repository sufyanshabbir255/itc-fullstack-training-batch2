# ===== IF statements =====
age = 44

if age >= 18:
    print("You are an adult")
else:
    print("You are under 18")

# if / elif / else
score = 72

if score >= 80:
    print("Grade: A")
elif score >= 60:
    print("Grade: B")
else:
    print("Grade: C")


# ===== FOR loops =====

# Loop through numbers 1 to 5
for number in range(1, 6):
    print("Number:", number)

# Loop through a list
fruits = ["apple", "banana", "mango"]

for fruit in fruits:
    print("I like", fruit)


# ===== IF inside a FOR loop =====
prices = [5, 12, 3, 20, 8]

for price in prices:
    if price > 10:
        print(price, "is expensive")
    else:
        print(price, "is cheap")

# Add up a total with a loop
total = 0
for price in prices:
    total = total + price
print("Total:", total)

# ===== WHERE =====

def Takeoff():
    num = 1
    while num <= 5:
        print(num)
        num = num + 1
        if num == 5 :
            print("Blast Off")
Takeoff()