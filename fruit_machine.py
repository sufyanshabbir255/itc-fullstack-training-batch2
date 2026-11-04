from random import randint
import sys

print('''
Welcome to the Fruit Machine!
Roll 2 fruits to win 50 credits
Roll 3 fruits to win 100 credits
Roll 3 bells to win 500 credits
But...
If you roll 2 skulls you lose 100 credits!
If you roll 3 skulls you lose ALL YOUR credits!
''')

def show_roll(roll):
    result_dict = {
         1: '🍒'
        ,2: '🔔'
        ,3: '🍋'
        ,4: '🍊'
        ,5: '⭐'
        ,6: '💀'
    }
    return f'You rolled: {result_dict[roll[0]]} {result_dict[roll[1]]} {result_dict[roll[2]]}.'

credit = 100

input('Press enter to pull the lever...')
while True:
    print(f'\nCurrent balance: {credit}')
    credit -= 20

    roll = (randint(1, 6), randint(1, 6), randint(1, 6))
    print(show_roll(roll))
    roll = sorted(roll)

    if len(set(roll)) == 1:
        if set(roll) == {6}:
            credit = 0
            print(f'You lost all your credits 💀')
        elif set(roll) == {2}:
            credit += 500
            print(f'You won 500 credits!')
        else:
            credit += 100
            print(f'You won 100 credits!')


    if roll[0] == roll[1] or roll[1] == roll[2]:
        if roll[0] != roll[2]:
            if roll[1] == 6:
                credit -= 100
                print(f'You lost 100 credits!')
            else:
                credit += 50
                print(f'You won 50 credits!')

    if roll[0] != roll[1] and roll[1] != roll[2]:
        print(f'You won nothing!')

    continue_playing = input('Press enter to continue or [Q] to quit...')
    if continue_playing.upper() == 'Q':
        print(f'Thank you for playing.\nYou finished with {credit} credits!')
        sys.exit()

    if credit <= 0:
        print('Game over! You have no credits left.\nThank you for playing!')
        sys.exit()