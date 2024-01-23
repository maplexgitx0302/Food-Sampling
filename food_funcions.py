"""Functions for food sampling.

Functions that related to:
- Read or modify `food.json` file.
- Sampling methods.
"""

import json

with open("food.json", "r") as json_file:
    # Read `food.json` file.
    food_json = json.load(json_file)

    # Maximum number of votes.
    max_choices = food_json["_max_choices"]

    # Create food option list.
    food_list = []
    for food in food_json.keys():
        if ("//" not in food) and (food[0] != "_"):
            # "//" represented comments in json files.
            food_list.append(food)
    food_indices = range(len(food_list))

    # Turn into dictionary with food indices.
    food_option_dict = dict(enumerate(food_list))


def change_max_choices(new_max_choices):
    global max_choices
    max_choices = new_max_choices


def print_food_options():
    """Print food options in `food.json` file."""

    global food_indices, food_option_dict
    print("# Table of food options:")
    for index in food_indices:
        food = food_option_dict[index]
        print(f"* {index} -> {food}")


class NumChoiceError(Exception):
    def __init__(self, num_choices, max_choices):
        """Too many choices."""

        error_message = (f"Over maximum number of choices -> "
                         f"{num_choices} > {max_choices}")
        super().__init__(error_message)


class WrongIndexError(Exception):
    def __init__(self, index):
        """Index does not exist."""

        error_message = f"Check your index -> {index}"
        super().__init__(error_message)


def check_vote_validity(vote: list[int]):
    """Check vote validity

    Args:
        vote : list[int]
            List of one's votes.

    Return:
        True if no errors are encountered, otherwise False.
    """

    if len(vote) > max_choices:
        raise NumChoiceError(len(vote), max_choices)

    for index in vote:
        if index not in food_indices:
            raise WrongIndexError(index)
