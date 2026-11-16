# def test(Age):
#     print("My age is {}".format(Age))
#     print("My age is " + str(Age))
#     print("My age is",Age)

# test(44)

def is_eligible(has_ticket, has_id, n):
    return (has_ticket and has_id) or (n>50 and n<80)
    return (has_ticket and has_id) or (50 < n < 80)


print(is_eligible(False, True, 50))