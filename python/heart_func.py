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
                if formula <= 0:  # 当小于等于0的时候，说明此时点(x,y)的位置是函数所包裹的位置（包括函数图像曲线（=0的时侯）），此时不用' '，用固定的某一个字母即可。
                    lst_con += char[x % len(char)]
                else:
                    lst_con += ' '
            lst.append(lst_con)  # 一行
            allChar += lst  # 所有行
        print('\n'.join(allChar))
        time.sleep(1)
        # x 定义宽 y定义高


def heart2():
    for s in "Dear I love you forever".split():
        print('\n'.join([''.join([(s[(x - y) % len(s)] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
                x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(12, -12, -1)]))
        time.sleep(1)


if __name__ == '__main__':
    heart()
