import time
import os


def heart():
    for char in "will be ok".split():
        lst_all_line = []
        for y in range(12, -12, -1):
            lst_line = []
            tmp_str = ''
            for x in range(-30, 30):
                cur = ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3
                if cur <= 0:  # 当小于等于0的时候，说明此时点(x,y)的位置是函数所包裹的位置（包括函数图像曲线（=0的时侯）），此时不用' '，用固定的某一个字母即可。
                    tmp_str += char[x % len(char)]
                else:
                    tmp_str += ' '
            lst_line.append(tmp_str)  # 一行
            lst_all_line += lst_line  # 所有行
        print(f'{os.linesep}'.join(lst_all_line))
        time.sleep(1)
        # x 定义宽 y定义高


def heart2():
    for s in "will be ok".split():
        print(f'{os.linesep}'.join([''.join([(s[(x - y) % len(s)] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
                x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(12, -12, -1)]))
        time.sleep(1)


if __name__ == '__main__':
    heart()

