import random

MAX_LINES = 3
MIN_BET = 1
MAX_BET = 100

ROWS = 3
COLS = 3

symbol_count = {  # total of symbols must be > (ROWS*COLS), otherwise, can crash (not enough symbols to fill slots).
    "\U0001F353": 3,
    "\U0001F95D": 3,
    "\U0001F34C": 3,
    "\U0001F347": 3
}

symbol_value = {
    "\U0001F353": 5,
    "\U0001F95D": 4,
    "\U0001F34C": 3,
    "\U0001F347": 2
}


def check_winning(columns, lines, bet, values):
    winnings = 0
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
    return winnings


def get_spin(rows, cols, symbols):
    all_symbols = []
    for symbol_code, symbol_digit in symbols.items():
        for _ in range(symbol_digit):
            all_symbols.append(symbol_code)
    #  print("all symbols...\n", all_symbols)  # test
    columns = []
    current_symbols = all_symbols[:]
    for _ in range(cols):
        column = []
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            #  print("removing...", current_symbols)  # test
            column.append(value)
        columns.append(column)
    #  print("\n after remove... ", current_symbols)  # test
    return columns


def print_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if is_integer(amount):
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Number must be greater than 0.")
        else:
            print("Please enter a number.")
    return amount


def get_lines(amount):
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if is_integer(lines):
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                if lines <= amount:
                    break
                else:
                    print("You do not have enough balance to bet on these lines."
                          f"\nYour current balance is: ${amount}.")
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    return lines


def get_bet():
    while True:
        amount = input(f"What would you like to bet on each line (${MIN_BET} - ${MAX_BET})? $")
        if is_integer(amount):
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Number must be between (${MIN_BET} - ${MAX_BET}).")
        else:
            print("Please enter a number.")
    return amount


def spin(balance):
    lines = get_lines(balance)
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough balance to bet that amount."
                  f"\nYour current balance is: ${balance}.")
        else:
            break
    print(f"You are betting ${bet} on {lines} lines.\nTotal bet: ${total_bet}")
    slots = get_spin(ROWS, COLS, symbol_count)
    print_machine(slots)
    winnings = check_winning(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}!")
    return winnings - total_bet


def main():
    balance = get_deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)
    print(f"You left with ${balance}")


main()
