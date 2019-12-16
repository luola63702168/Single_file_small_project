from matplotlib import pyplot as plt
# import random
from matplotlib import font_manager

# matplotlib默认不支持中文字符，因为默认的英文字体无法显示汉字
# 设置中文字体（指定具体的字体文件路径，然后再需要显示中文的地方添加fontproperties参数）
my_font = font_manager.FontProperties(fname=r"C:\Windows\Fonts\MSYH.TTC")

# figure图形图标的意思在这里指的就是我们画的图
# 通过实例化一个figure并且传递参数，能够在后台自动使用该figure实例
# 在图像模糊的时候可以传入dpi参数，让图片更加清晰
fig = plt.figure(figsize=(15, 6), dpi=80)

# 数据在x轴的一个位置，是一个可迭代对象
x = range(2, 26, 2)
# 数据在y轴的一个位置
y = [15, 13, 14.5, 17, 20, 25, 26, 26, 27, 22, 18, 15]

# 获取最大值最小值的索引
max_indx = y.index(max(y))
min_indx = y.index(min(y))
# 传入x和y，通过plot绘制折线图

# 设置线条样式，颜色，透明度
plt.plot(x, y, label="温度", linestyle="-.", color="red", alpha=0.5)
# 通过plot函数的label设置图例
plt.legend(prop=my_font, loc="best")

# 设置最大值
plt.plot(x[max_indx], y[max_indx], 'ks')
# 显示最大值
show_max = '[' + str(x[max_indx]) + ',' + str(y[max_indx]) + ']'
plt.annotate(show_max, xytext=(x[max_indx], y[max_indx]), xy=(x[max_indx], y[max_indx]))  # annotate用于在图形上给数据添加文本注解

# 设置最小值
plt.plot(x[min_indx], y[min_indx], 'gs')
# 显示最小值
show_min = '[' + str(x[min_indx]) + ',' + str(y[min_indx]) + ']'
plt.annotate(show_min, xytext=(x[min_indx], y[min_indx]), xy=(x[min_indx], y[min_indx]))

# 设置水印
fig.text(0.75, 0.45, 'hello world',
         fontsize=40, color='gray',
         ha='right', va='bottom', alpha=0.4)

# 设置x轴的刻度
x_ticks = ["X日{}点".format(i) for i in x]
plt.xticks(x, x_ticks, rotation=45, fontproperties=my_font)

# 设置x轴，y轴的标注，标题
plt.xlabel("时间", fontproperties=my_font)
plt.ylabel("温度", fontproperties=my_font)
plt.title("一天的温度的变化", fontproperties=my_font)
# 设置网格
plt.grid()
plt.show()

# Axes.annotate(s, xy, *args, **kwargs)方法介绍
# 参考：https://blog.csdn.net/leaf_zizi/article/details/82886755

# 其它类型的画图用例均可参考。