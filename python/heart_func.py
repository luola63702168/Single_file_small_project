import time


def heart():
    sentence = "Dear I love you forever"
    for char in sentence.split():
        allChar = []
        for y in range(12, -12, -1):
            lst = []
            lst_con = ''
            for x in range(-30, 30):
                formula = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
                if formula <= 0:
                    lst_con += char[x % len(char)]
                else:
                    lst_con += ' '
            lst.append(lst_con)
            allChar += lst
        print('\n'.join(allChar))
        time.sleep(1)


def heart2():
    for s in "Dear I love you forever".split():
        print('\n'.join([''.join([(s[(x - y) % len(s)] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
                x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(12, -12, -1)]))
        time.sleep(1)


if __name__ == '__main__':
    heart()
