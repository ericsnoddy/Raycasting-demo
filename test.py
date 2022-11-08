from random import randrange, random

accuracy = (10, 25)
roll_goal = randrange(accuracy[0], accuracy[1] + 1) / 100
roll = random()

if roll < roll_goal:
    print(f'hit - {roll} < {roll_goal}')
else:
    print(f'miss - {roll} > {roll_goal}')