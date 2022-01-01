#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>


// Prototypes
void toArray(int arr[], long num);
int digit_sum(long num);
bool isAMEX(const int *numberArray, const int numberOfDigits);
bool isMASTERCARD(const int *numberArray, const int numberOfDigits);
bool isVISA(const int *numberArray, const int numberOfDigits);

int main(void)
{
    long credit_card_number;
    int numberOfDigits;
    bool isValid = false;
    while (!isValid)
    {
        credit_card_number = get_long("Number: ");
        numberOfDigits = floor(log10(credit_card_number)) + 1;
        if (numberOfDigits != 13 && numberOfDigits != 15 && numberOfDigits != 16)
        {
            printf("INVALID\n");
            return 0;
        }
        else
        {
            isValid = true;
        }
    }

    int numberArray[100];
    toArray(numberArray, credit_card_number);

    /* Luhn's Algorithm */

    // Step 1
    int sum = 0;
    for (int i = (numberOfDigits - 1) - 1; i >= 0; i -= 2)
    {
        sum += digit_sum(numberArray[i] * 2);
    }

    // Step 2
    for (int i = (numberOfDigits - 1); i >= 0; i -= 2)
    {
        sum += numberArray[i];
    }

    // Step 3
    int lastDigit = sum % 10;
    if (lastDigit != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        //int startNumbers = numberArray[0] * 10 + numberArray[1];
        if (isAMEX(numberArray, numberOfDigits))
            //if ((numberOfDigits == 15) && (startNumbers == 34 || startNumbers == 37))
        {
            printf("AMEX\n");
        }
        else if (isMASTERCARD(numberArray, numberOfDigits))
            //else if ((numberOfDigits == 16) && (startNumbers >= 51 && startNumbers <= 55))
        {
            printf("MASTERCARD\n");
        }
        else if (isVISA(numberArray, numberOfDigits))
            //else if ((numberOfDigits == 13 || numberOfDigits == 16) && (numberArray[0] == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

    return 0;
}


void toArray(int arr[], long num)
{
    int numberOfDigits = floor(log10(num)) + 1;
    for (int i = 0; i < numberOfDigits; ++i)
    {
        arr[(numberOfDigits - 1) - i] = num % 10;
        num /= 10;
    }
}


int digit_sum(long num)
{
    int sum = 0;
    while (num)
    {
        sum += (num % 10);
        num = num / 10;
    }
    return sum;
}

bool isAMEX(const int *numberArray, const int numberOfDigits)
{
    return (numberOfDigits == 15) && strchr("3", numberArray[0] + '0') && strchr("47", numberArray[1] + '0');
}

bool isMASTERCARD(const int *numberArray, const int numberOfDigits)
{
    return (numberOfDigits == 16) && strchr("5", numberArray[0] + '0') && strchr("12345", numberArray[1] + '0');
}

bool isVISA(const int *numberArray, const int numberOfDigits)
{
    return (numberOfDigits == 13 || numberOfDigits == 16) && strchr("4", numberArray[0] + '0');
}