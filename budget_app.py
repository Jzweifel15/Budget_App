class Category:

    def __init__(self, desc):
        self.desc = desc
        self.ledger = []
        self.balance = 0.0


    def __str__(self):
        header = self.desc.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            # format description and amount
            line_desc = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            # Truncate ledger description and amount to 23 and 7 characters respectively
            ledger += "{}{}\n".format(line_desc[:23], line_amount[:7])

        total = "Total: {:.2f}".format(self.balance)
        return header + ledger + total


    def deposit(self, amount, desc=""):
        self.ledger.append({"amount": amount, "description": desc})
        self.balance += amount


    def withdraw(self, amount, desc=""):
        if self.balance - amount >= 0:
            self.ledger.append({"amount": -1 * amount, "description": desc})
            self.balance -= amount

            return True
        else:
            return False


    def get_balance(self):
        return self.balance


    def transfer(self, amount, new_category):
        if self.withdraw(amount, "Transfer to {}".format(new_category.desc)):
            new_category.deposit(amount, "Transfer from {}".format(self.desc))

            return True
        else:
            return False


    def check_funds(self, amount):
        if self.balance >= amount:
            return True
        else:
            return False



def create_spend_chart(categories):
    spent_amounts = []
    # Get total spent in each category
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    # Calculate percentage rounded down to the nearest 10
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    # Create the bar chart substrings
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.desc, categories))
    max_length = max(map(lambda desc: len(desc), descriptions))
    descriptions = list(map(lambda desc: desc.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")