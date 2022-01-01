def compute_grade(text: str):
    """ Compute readability level needed to comprehend the text using Coleman–Liau index """

    countOfLetters = 0
    countOfWords = 0
    countOfSentences = 0

    for c in text:
        if c.isalpha():
            countOfLetters += 1
        if c.isspace():
            countOfWords += 1
        if (c in ['.', '?', '!']):
            countOfSentences += 1

    # Last word in the last sentence will not be detected. We need to manaully account for it!
    countOfWords += 1

    print(f"{countOfLetters} letter(s)")
    print(f"{countOfWords} word(s)")
    print(f"{countOfSentences} sentence(s)")

    L = (countOfLetters / countOfWords) * 100
    S = (countOfSentences / countOfWords) * 100

    # The Coleman-Liau formula
    grade = round(0.0588 * L - 0.296 * S - 15.8)

    return grade


def main():
    text = input("Text: ")
    grade = compute_grade(text)
    if (grade >= 16):
        print("Grade 16+")
    elif (grade < 1):
        print("Before Grade 1")
    else:
        print("Grade", grade)


if __name__ == "__main__":
    main()