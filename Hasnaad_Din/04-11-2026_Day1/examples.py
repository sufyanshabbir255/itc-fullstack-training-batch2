def sumList(numbers):
    total = 0                # start at zero
    for item in numbers:
        total += item        # add this number to the running total
    return total             # after the loop, return the total

#print(sumList([1, 2, 3]))    # 6

fruits = ["Apple", "Pear","Orange"] # list

print(fruits[1])

for fruit in fruits:
    print(fruit)

names = {"Ayla", "Alyan","Safa"}  # set

print(names)