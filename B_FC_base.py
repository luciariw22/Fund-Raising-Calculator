# import libraries


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


def instructions():
    print('''
    
ℹℹℹℹℹ Instructions ℹℹℹℹℹℹ

Instructions go here
    
    ''')


# Main routine goes here

want_help = yes_no("Do you want to read the instructions? ")
if want_help == "yes":
    instructions()

get_int = num_check("How many do you need? ",
                    "Please enter an amount more than 0\n",
                    int)
get_cost = num_check("How much does it cost? $",
                     "Please enter a number more than 0\n",
                     float)

print("You need: {}".format(get_int))
print("It costs: ${}".format(get_cost))
