# 1 - add numbers
def add_numbers(a, b): # parameters
    return a + b
print(add_numbers(5, 3))

# 2 - show names
def show_names(first, last):
    return f"{first} {last}"

print(show_names("Hasnaad", "Din"))

# 3 - add vat
def add_vat(price):
    return price * 1.2

print(add_vat(100))

# 4 - swap variables
def swap_variables(a,b):
    return(b,a)

a = "Hasnaad"
b = "Din"

#a,b = swap_variables(a, b)
a,b = b,a
print (a,b)



# 5 - count number of letters in text
def count_letters(text):
    return len(text)

print (count_letters("Hasnaad"))

#Anil's Solution

# logic a, b;
# logic temp;

# temp = a;
# a = b;
# b = temp;

