import json


def show_ingredients():
    """
    Allows the user to see what the acceptable ingredients are in a list and prints
    out the possible ingredients that the user can input.
    """
    # Check if use wants to see the ingredients.
    user_show_ingredients = str(input("\nWould you like to first see a list of all possible ingredients? (Yes / No): "))

    if user_show_ingredients == "Yes" or user_show_ingredients == "yes":
        all_ingredients = []

        # Open the Cocktails.json file to read.
        with open('Cocktails.json', 'r') as infile:
            cocktails_dict = json.load(infile)

        # Add each possible ingredient from the JSON file to all_ingredients.
        for cocktail in cocktails_dict:
            for ingredient in cocktail["ingredients"]:
                if "ingredient" in ingredient and ingredient["ingredient"] not in all_ingredients:
                    all_ingredients.append(ingredient["ingredient"])

        # Printing the list of possible ingredients.
        print("\nHere are the acceptable ingredients:\n")
        line_length = 0
        for ingredient in all_ingredients:
            if line_length <= 40:
                print(f"{ingredient} |", end=" ")
                line_length += len(ingredient)
            else:
                print(ingredient + " |")
                line_length = 0
        print("\n")
    return


def show_garnishes():
    """
    Allows the user to see what the acceptable garnishes are in a list and
    prints out the possible garnishes that the user can input.
    """
    # Check if use wants to see the garnishes.
    user_show_garnishes = str(input("\nWould you like to first see a list of all possible garnishes? (Yes / No): "))

    if user_show_garnishes == "Yes" or user_show_garnishes == "yes":
        all_garnishes = []

        # Open the Cocktails.json file to read.
        with open('Cocktails.json', 'r') as infile:
            cocktails_dict = json.load(infile)

        # Add each possible garnish from the JSON file to all_garnishes.
        for cocktail in cocktails_dict:
            if "garnish" in cocktail and cocktail["garnish"] not in all_garnishes:
                all_garnishes.append(cocktail["garnish"])

        # Printing the list of possible garnishes.
        print("\nHere are the acceptable garnishes:\n")
        line_length = 0
        for garnish in all_garnishes:
            if line_length <= 40:
                print(f"{garnish} |", end=" ")
                line_length += len(garnish)
            else:
                print(garnish + " |")
                line_length = 0
        print("\n")
    return


def show_categories():
    """
    Allows the user to see what the acceptable categories are in a list and
    prints out the possible categories that the user can input.
    """
    # Check if use wants to see the categories.
    user_show_categories = str(input("\nWould you like to first see a list of all possible categories? (Yes / No): "))

    if user_show_categories == "Yes" or user_show_categories == "yes":
        all_categories = []

        # Open the Cocktails.json file to read.
        with open('Cocktails.json', 'r') as infile:
            cocktails_dict = json.load(infile)

        # Add each possible garnish from the JSON file to all_categories.
        print("\nHere are the acceptable categories:\n")
        for cocktail in cocktails_dict:
            if "category" in cocktail and cocktail["category"] not in all_categories:
                all_categories.append(cocktail["category"])
        for category in all_categories:
            print(f"{category} |", end=" ")
        print("\n")
    return


def cocktail_search(user_ingredients_list, user_garnish_list, user_desired_category, user_servings):
    """
    Determines which cocktails in Cocktails.json that the user can make given their input parameters.
    :param user_ingredients_list: List of ingredients from user.
    :param user_garnish_list:  List of garnishes from user.
    :param user_desired_category: Desired category of cocktail for the user.
    :param user_servings: Number of servings the user wants to make.
    :return: Printed list of cocktails with glasses, ingredients, garnishes, and preparation.
    """
    # Initialize the possible cocktails and number of possible cocktails.
    possible_cocktails = dict()
    number_of_cocktails = 0

    # Open the Cocktails.json file to read.
    with open('Cocktails.json', 'r') as infile:
        cocktails_dict = json.load(infile)

    # Search the JSON file for the ingredients in user_ingredients_list.
    for entry in cocktails_dict:
        sufficient_ingredients = True
        # Check if user has sufficient ingredients for cocktail entries.
        for ingredient in entry["ingredients"]:
            if "ingredient" in ingredient and sufficient_ingredients is True and ingredient["ingredient"] not in user_ingredients_list:
                sufficient_ingredients = False
        # Check if user has sufficient garnishes for cocktail.
        if "garnish" in entry and entry["garnish"] not in user_garnish_list:
            sufficient_ingredients = False
        # User has sufficient ingredients for given cocktail, add to the dictionary of possible cocktails.
        if sufficient_ingredients is True:
            # Some cocktails have no garnishes.
            if entry.get("garnish") is None:
                entry["garnish"] = "None"
            # Check if cocktail is of the specified category.
            if len(user_desired_category) == 0 or entry["category"] in user_desired_category:
                possible_cocktails[entry["name"]] = \
                    [entry["glass"], entry["category"], entry["ingredients"], entry["garnish"], entry["preparation"]]
                number_of_cocktails += 1

    # If user does not have enough ingredients for any cocktails, prints out following message.
    if len(possible_cocktails) == 0:
        print("\nSadly, your listed ingredients are not sufficient to make any of the cocktails in our recipe book. "
              "Better run to the store!")
        if user_garnish_list != []:
            try_again = input("It appears you entered garnishes, would you like to search again without garnishes? "
                              "Besides, who needs those frills anyway... (Yes / No): ")
            if try_again.capitalize() == "Yes":
                all_garnishes = []
                # Open the Cocktails.json file to read.
                with open('Cocktails.json', 'r') as infile:
                    cocktails_dict = json.load(infile)

                # Add each possible garnish from the JSON file to all_garnishes.
                for cocktail in cocktails_dict:
                    if "garnish" in cocktail and cocktail["garnish"] not in all_garnishes:
                        all_garnishes.append(cocktail["garnish"])
                cocktail_search(user_ingredients_list, all_garnishes, user_desired_category, user_servings)
    # User can make certain cocktails, prints out cocktail names and corresponding information.
    else:
        print(f"\nParty time! You can make {str(number_of_cocktails)} cocktail(s) to serve your group "
              f"of {str(user_servings)}:\n")
        for cocktail in possible_cocktails:
            print(
                cocktail + ":\n" +
                "\t" + "Category: " + possible_cocktails[cocktail][1] + "\n"
                "\t" + "Glass Type: " + possible_cocktails[cocktail][0] + "\n"
                "\t" + f"Ingredients to Serve {user_servings}: "
            )
            for items in possible_cocktails[cocktail][2]:
                # Convert to fluid ounces.
                if "amount" in items:
                    amount = round(user_servings * items["amount"] * 0.33814, 1)
                    ingredient = str(items["ingredient"])
                    # Some syrup ingredients are specified with labels, so must be converted.
                    if "label" in items:
                        ingredient = items["label"]
                    print("\t" + "\t" + f"{str(amount)} fl oz of {ingredient}")
                if "special" in items:
                    # Convert first digit in to match number of servings.
                    if items["special"][0].isdigit() is True:
                        items["special"] = str(4 * int(items["special"][0])) + items["special"][1:]
                    special = str(items["special"])
                    print("\t" + f"Optional Special Ingredient: {special}")
            print(
                "\t" + "Garnish: " + possible_cocktails[cocktail][3] + "\n"
                "\t" + "Preparation: " + possible_cocktails[cocktail][4] + "\n"
            )
    return
