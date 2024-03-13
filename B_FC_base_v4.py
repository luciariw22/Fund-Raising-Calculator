# import libraries
import pandas
import math


# functions go here

# checks that input is either a float or an
# integer that is more than zero. Takes in custom error message
def num_check(question, error, num_type):
    valid = False

    while not valid:

        try:
            response = num_type(input(question))

            if response <= 0:
                print(error)

            else:
                return response

        except ValueError:
            print(error)


# checks that user has entered y / n to a question
def yes_no(question):
    to_check = ["yes", "no"]

    valid = False
    while not valid:

        response = input(question).lower()

        for var_item in to_check:
            if response == var_item:
                return response
            elif response == var_item[0]:
                return var_item

        print("Please enter either yes or no...\n")


# checks users answer isn't blank
def not_blank(question, error):
    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print("{}. \nPlease try again.\n".format(error))
            continue

        return response


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# gets expenses, returns list which has
# the data frame and subtotal
def get_expenses(var_fixed):
    # Set up dictionaries and lists

    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # loop to get component, quantity and price
    item_name = ""
    while item_name.lower() != "xxx":

        print()
        # get name, quantity and item
        item_name = not_blank("Item name: ",
                              "The component name can't be "
                              "blank.")
        if item_name.lower() == "xxx":
            break

        if var_fixed == "variable":
            quantity = num_check("Quantity:",
                                 "The amount must be a whole number "
                                 "more than zero",
                                 int)
        else:
            quantity = 1

        price = num_check("How much for a single item? $",
                          "The price must be a number <more "
                          "than 0>",
                          float)

        # add item, quantity, and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    expense_frame = pandas.DataFrame(variable_dict)
    expense_frame = expense_frame.set_index('Item')

    # Calculate cost of each component
    expense_frame['Cost'] = expense_frame['Quantity'] \
                            * expense_frame['Price']

    # Find sub-total
    sub_total = expense_frame['Cost'].sum()

    # Currency formatting (uses currency function)
    add_dollars = ['Price', 'Cost']
    for item in add_dollars:
        expense_frame[item] = expense_frame[item].apply(currency)

    return [expense_frame, sub_total]


# Prints expense frames
def expense_print(heading, frame, subtotal):
    print()
    print("**** {} Costs ****".format(heading))
    print(frame)
    print()
    print("{} Costs: ${:.2f}".format(heading, subtotal))
    return ""


# work out profit goal and total sales required
def profit_goal(total_costs):
    # Initialise variables and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # ask for profit goal...
        response = input("What is your profit goal (eg $500 or 50%) ")

        # check if first character is $...
        if response[0] == "$":
            profit_type = "$"
            # Get amount (everything after the $)
            amount = response[1:]

        # check if lsat character is %
        elif response[-1] == "%":
            profit_type = "$"
            # get amount (everything before the %)
            amount = response[:-1]

        else:
            # set response to amount for now
            profit_type = "unknown"
            amount = response

        try:
            # check amount is more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no("Do you mean ${:.2f}. ie {:.2f} dollars? ,"
                                 "y / n ".format(amount, amount))

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount < 100:
            percent_type = yes_no("Do you mean {}%? ,"
                                  "y / n".format(amount))
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# rounding function
def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to


# Main routine goes here
# get product name
product_name = not_blank("Product name: ", "The product name can't be blank. ")
how_many = num_check("How many items will you be producing? "
                     "The number of items must be a whole "
                     "number more than zero", "Please enter a number more than 0", int)

print()
print("Please enter your variable costs below...")
# Get variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

print()
have_fixed = yes_no("Do you have fixed costs (y / n)? ")

if have_fixed == "yes":
    # Get fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]

else:
    fixed_sub = 0
    fixed_frame = ""

# work out total costs and profit target
all_costs = variable_sub + fixed_sub
profit_target = profit_goal(all_costs)

# Calculates total sales needed to reach goal
sales_needed = all_costs + profit_target

# Ask user for rounding
round_to = num_check("Round to nearest...? ", "Can't be 0", int)

# Calculate recommended price
selling_price = sales_needed / how_many
print("Selling Price (unrounded): ${:.2f}".format(selling_price))

recommended_price = round_up(selling_price, round_to)

# write data to file

# Change frames to strings
variable_txt = pandas.DataFrame.to_string(variable_frame)

if have_fixed == "yes":
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
else:
    fixed_txt = ""

# **** Printing area ****

print()
product_heading = "**** Fund Raising - {} ****".format(product_name)
print()
# expense_print("Variable", variable_frame, variable_sub)
#
# if have_fixed == "yes":
#     expense_print("Fixed", fixed_frame, fixed_sub)

# print()
# print("**** Total Costs: ${:.2f} ****".format(all_costs))
# print()
#
# print()
variable_heading = "===== Variable Costs ====="
fixed_heading = "===== Fixed Costs ====="
sales_heading = "**** Profit & Sales Targets *****"
profit_target_text = f"Profit Target: ${profit_target:.2f}"
required_sales = f"Total Sales: ${all_costs + profit_target:.2f}"
#
# print()
#
recommendation_heading = "===== Recommendations ====="
# print("Minimum Price: ${:.2f}".format(selling_price))
recommended_price_string = "Recommended Price: ${:.2f}".format(recommended_price)
#
# print(variable_frame)

to_write = [product_heading, variable_heading, variable_txt,
            fixed_heading, fixed_txt, sales_heading,
            profit_target_text, required_sales,
            recommendation_heading, recommended_price_string]


# Write to file...
# create file to hold data (add. txt extension)
file_name = "{}.txt".format(product_name)
text_file = open(file_name, "w+")

# heading
for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()

# Print stuff
for item in to_write:
    print(item)
    print()


