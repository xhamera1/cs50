def get_string(prompt):
    return str(input(prompt))

all_text = get_string("Text: ")
lenght = len(all_text)
sentence_count = 0
letter_count = 0
word_count = 1
list_text = list(all_text)
for i in range (0, lenght):
    if list_text[i] == '.'  or list_text[i] == '!' or list_text[i] == '?' :
            sentence_count += 1
    if list_text[i].isalpha() == True:
         letter_count += 1
    if list_text[i] == ' ':
         word_count += 1

L = float(letter_count/word_count) * 100
S = float(sentence_count/word_count) * 100

grade = 0.0588 * L - 0.296 * S - 15.8
result = round(grade)
if result<1:
    print("Before Grade 1")
elif result>=16:
    print("Grade 16+")
else:
    print(f"Grade {result}");

