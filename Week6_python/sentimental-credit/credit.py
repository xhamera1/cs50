def get_string(prompt):
    return str(input(prompt))

number = get_string("Number: ")
copy_number = number

if len(number) != 15 and len(number) != 16 and len(number) != 13:
    print("INVALID")
else:
    number_list = list(number)
    sum_2x = 0
    sum_1x = 0

    for i in range(len(number) - 2, -1, -2):
        x = 2 * int(number_list[i])
        sum_2x += x // 10 + x % 10

    for i in range(len(number) - 1, -1, -2):
        sum_1x += int(number_list[i])

    total_sum = sum_1x + sum_2x

    if total_sum % 10 != 0:
        print("INVALID")
    else:
        if number[0] == '4':
            print("VISA")
        elif (number[0] == '3' and number[1] == '4') or (number[0] == '3' and number[1] == '7'):
            print("AMEX")
        elif (number[0] == '5' and (number[1] == '1' or number[1] == '2' or number[1] == '3' or number[1] == '4' or number[1] == '5')):
            print("MASTERCARD")
        else:
            print("INVALID")
