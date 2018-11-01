"""
Simple examples to explore Python
"""

# Strings


"cooperate"
"defect"
print("cooperate")
len("cooperate")
type("cooperate")
3 * ("cooperate")


# Numbers


3 + 5
5 - 3
5 / 3
5 // 3
3 * 5
3 ** 5
type(3)
type(1.66)
abs(-2)


# Working with strings and numbers


"cooperate"[0]
"cooperate"[8]
"cooperate"[-1]
"cooperate"[0:3]
"cooperate"[:-1]
"cooperate"[::-1]
"cooperate".index("c")
"cooperate".count("o")


# Variables


cooperate = 3
defect = 5
print(defect + cooperate)
cooperate = defect
print(defect)
defect += 10
choice = "cooperate"
print(choice)


# Special Variables - Booleans and None


3 == 3
3 == 5
type(3 == 3)
3 > 5
3 < 5
3 != 5
3 <= 3
5 >= 3
5 is 3
5 is not 3

player_one = None
type(player_one)
print(player_one)


# Conditionals - if


cooperate = 3
if cooperate == 3:
    print("Cooperators get 3")

defect = 5
if defect > 3:
    print("You'd better defect")

# Conditionals - if and else

if cooperate > 3:
    print("Okay, cooperate")
else:
    print("I'll defect")

if cooperate > 3:
    print ("Okay, cooperate")
else:
    pass

# Conditionals - if, else and elif

cooperate = 0
if cooperate > 3:
    print("Okay, cooperate")
elif cooperate == 0:
    print("We're all doomed")
else:
    print("I'll defect")


# Iteration


for i in range(5):
    print("Still going")

state = "ongoing"
i = 0
while state != "end":
    print("waiting")
    i += 1
    if i == 5:
        state = "end"  # could also use break


# Data structures - lists

payoffs = [3, 0, 5, 1]
payoffs[0]
payoffs[0] = 99
print(payoffs)
payoffs.append(55)
print(payoffs)
payoffs.index(0)


# Looping over lists


for e in payoffs:
    print(e*2)

[e*2 for e in payoffs]
[e for e in payoffs if e > 1]


# Data structures - dictionaries

payoff_dict = {"cooperate" : 3, "defect" : 5}
payoff_dict["cooperate"]
payoff_dict["defect"]

payoff_dict.keys()
payoff_dict.values()
payoff_dict.items()
payoff_dict["nukes"] = 0
print(payoff_dict
"cheat" in payoff_dict


# Looping over dictionaries


for k, v in payoff_dict.items():
    print(k, v)

{k : v*2 for (k, v) in payoff_dict.items()}


# Functions


def even_payoffs(x):
    '''
    takes a list as input and returns a new list containing only even values
    '''

    even = [e for e in x if e%2 == 0]
    return even

even_payoffs([3, 5, 0, 1])


# Recursion


def factorial(x):
    if x == 1:
        return 1
    else:
        return x*factorial(x-1)


# Modules, packages, libraries


import random
random.randrange(0, 10)

from random import randrange
randrange(0, 10)

dir(random)


# Object oriented programming

class Communication(object):
    pass

class Communication(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

c = Communication("Nitze", "Herter")
c.x

class Communication(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def allies(self, other):
        allies1 = [self.x, other.x]
        allies2 = [self.y, other.y]
        return allies1, allies2

c = Communication("Nitze", "Herter")
d = Communication("Mickey", "Donald")

c.allies(d)
d.allies(c)
