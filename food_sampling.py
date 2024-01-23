"""Main script for food sampling.

How to use?
>> In your terminal, simply run with
```bash
python food_sampling.py
```

Where can I find the food options?
>> All food options are stored in `food.json` file.
"""

from functools import reduce
import os
import random

import food_funcions as ff


def print_info():
    """Print rules and commands."""

    print()
    print("# Welcome to food sampling!")
    print("# Start voting, e.g., 1 1 2 or 0 8 (seperate with spaces)")
    print("# Type '-1' to stop inputing.")
    print("# Type '-t' to show the food table again.")
    print("# Type '-r' to restart voting.")
    print("# Type '-z' to undo the last voting.")
    print("# Type '-72' to choose 72.")


def clear_line(n=1):
    """Clear n lines."""

    for _ in range(n):
        print('\033[1A\033[K', end='')


def clear_all():
    """Clear all."""

    if os.name == "nt":
        # Windows system.
        def clear():
            return os.system('cls')
    else:
        # Other unix-like systems
        def clear():
            return os.system('clear')

    clear()


# Prepare for a new vote.
weights = []  # For storing votes.
ielector = 1  # For elector (voter) counting.
error_flag = False  # Detecting whether an error occurred.


def init_vote():
    """Function for initializing a new vote."""

    # Reinitialize.
    global weights, ielector, error_flag
    weights = []
    ielector = 1
    error_flag = False

    # Print information.
    print_info()
    print("\n ========= Voting Start ========= \n")


# Start voting.
init_vote()

while True:
    # Input prompt.
    prompt = f"(Voter #{ielector}) Vote for your choice: "
    vote = input(prompt).lower()

    # Clean up prints.
    clear_line(n=1)
    if error_flag:
        clear_line(n=2)
        error_flag = False

    if vote == "-1":
        # Finish voting.
        print(" ========= Voting Done  =========\n")
        print(f"Total Electors: {ielector - 1}")
        break

    elif vote == "-t":
        # Print food option table.
        ff.print_food_options()
        print()

    elif vote == "-r":
        # Restart a vnew vote.
        clear_all()
        init_vote()

    elif vote == "-z":
        # Undo last vote.
        weights = weights[:-1]
        ielector -= 1

    elif vote == "-72":
        # Just eat 72!
        weights = [[0, 0, 0]]
        break

    else:
        # Normal votes.
        try:
            vote = vote.split()
            vote = list(map(int, vote))
            ff.check_vote_validity(vote)

        except Exception as e:
            error_flag = True
            print(f"ERROR: {e}\n")

        else:
            weights.append(vote)
            ielector += 1


# Calculating weights.
if len(weights) == 0:
    print("\n# No weights specified -> uniform weights.")
    weights = list(ff.food_indices)

else:
    weights = reduce(lambda x, y: x + y, weights)
    weights.sort()

print(f"\n# Total weights = {weights}\n")

for index, food in ff.food_option_dict.items():
    num_votes = weights.count(index)
    if num_votes > 0:
        print(f"* {food} has {num_votes} vote(s).")

# Samples.
print("\n# Sampling result:")
candidates = []
while len(candidates) < min(3, len(set(weights))):
    sample = ff.food_option_dict[random.sample(weights, k=1)[0]]
    if sample not in candidates:
        candidates.append(sample)
        print(f"* Number {len(candidates)} food candidate is {sample}")
