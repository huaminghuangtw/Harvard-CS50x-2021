from dataclasses import dataclass
import sys
import math
import re


# https://stackoverflow.com/questions/35988/c-like-structures-in-python
@dataclass
class credit_card:
    credit_card_number: str
    numberArray: list
    numberOfDigits: int


def digit_sum(num):
    sum = 0
    while num:
        sum += (num % 10)
        num = num // 10
    return sum


def isAMEX(numberArray: list, numberOfDigits: int):
    return (numberOfDigits == 15) and (numberArray[0]*10 + numberArray[1] in [34, 37])


def isMASTERCARD(numberArray: list, numberOfDigits: int):
    return (numberOfDigits == 16) and (51 <= numberArray[0]*10 + numberArray[1] <= 55)


def isVISA(numberArray: list, numberOfDigits: int):
    return (numberOfDigits in [13, 16]) and (numberArray[0] == 4)


def check_credit_card_type(c: credit_card):
    """ Luhn's Algorithm """

    # Step 1
    sum = 0
    for i in range((c.numberOfDigits - 1) - 1, -1, -2):
        sum += digit_sum(c.numberArray[i] * 2)

    # Step 2
    for i in range(c.numberOfDigits - 1, -1, -2):
        sum += c.numberArray[i]

    # Step 3
    lastDigit = sum % 10
    if (lastDigit != 0):
        print("INVALID")
    else:
        startNumbers = c.numberArray[0] * 10 + c.numberArray[1]
        if isAMEX(c.numberArray, c.numberOfDigits):
            print("AMEX")
        elif isMASTERCARD(c.numberArray, c.numberOfDigits):
            print("MASTERCARD")
        elif isVISA(c.numberArray, c.numberOfDigits):
            print("VISA")
        else:
            print("INVALID")


def main():
    while (True):
        credit_card_number = input("Number: ")
        if (not re.match("^(\d{13}|\d{15}|\d{16})$", str(credit_card_number))):   # regular expression (\d = [0-9])
            print("INVALID")
            sys.exit(0)   # Or: return
        else:
            numberArray = [int(digit) for digit in credit_card_number]   # list comprehension
            numberOfDigits = math.floor(math.log10(int(credit_card_number))) + 1
            c = credit_card(credit_card_number, numberArray, numberOfDigits)
            break

    check_credit_card_type(c)


if __name__ == "__main__":
    main()