from cs50 import get_string


def main():
    text = get_string("Text: ")
    letters = 0
    words = 1       # to account for first word
    sentences = 0
    
    length = len(text)

    # variables for conditions
    i = 0
    j = 0
    k = 0
    
    # conditions
    for i in range(length):
        if text[i].isalpha():
            letters = letters + 1
            
    for j in range(length):
        if text[j].isspace():
            words = words + 1

    for k in range(length):
        if text[k] == "." or text[k] == "!" or text[k] == "?":
            sentences = sentences + 1

    print(letters, words, sentences)
    # converting  integers to float
    l = float(letters)
    w = float(words)
    s = float(sentences)
    
    # average letters per 100 words
    L = float((l * (100 / w)))
    
    # average sentences per 100 words
    S = float((s * (100 / w)))
    
    # Coleman-liau formula
    index = float((0.0588 * L) - (0.296 * S) - 15.8)
    
    # round to whole number
    grade = int(round(index))
    
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print("Grade ", grade)


main()