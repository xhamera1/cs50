def get_int_max8(prompt):
    while True:
        try:
            x = int(input(prompt))
            if x<1 or x>8 :
                raise ValueError
            return x
        except ValueError:
            pass

n = get_int_max8("Height: ")
line = ' ' * (n+3)
line_list = list(line)
line_list[n+2] = '#'
for i in range(n-1, -1, -1):
    line_list[i] = '#'
    line = ''.join(line_list)
    line_list.append('#')
    print(line)

