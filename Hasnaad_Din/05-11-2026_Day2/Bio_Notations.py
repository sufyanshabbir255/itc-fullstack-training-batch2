#O(1) - Constant Time
def get_first(lst):
    return lst[0]

lst = [1,2,3]
print(get_first(lst))

#O(n) - Linear Time
def print_list(lst):
    for item in lst:
        print(item)

lst = [1,2,3]
print_list(lst)

#O(n²) - Quadratic Time - Nested Loops
def pairs(n):
    for i in range(n):
        for j in range(n):
            print(i, j)

pairs(2)