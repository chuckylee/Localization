import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# a = [13.895216400911162, 30.751708428246015, 29.612756264236904, 13.66742596810934,
#      5.694760820045558, 3.8724373576309796, 1.5945330296127562, 0.9111617312072893, 0.0, 0.0, 0]
# a = [15.945330296127562, 41.913439635535305, 25.968109339407746, 7.289293849658314,
#      6.605922551252847, 1.5945330296127562, 0.683371298405467, 0.0, 0.0, 0.0, 0]
# a = [11.46788990825688, 23.853211009174313, 30.73394495412844, 20.642201834862384, 5.504587155963303,
#      4.81651376146789, 2.293577981651376, 0.22935779816513763, 0.45871559633027525, 0.0, 0]
# b = [10.068649885583524, 31.57894736842105, 31.35011441647597, 17.391304347826086, 5.034324942791762,
#      1.6018306636155606, 1.8306636155606408, 0.9153318077803204, 0.2288329519450801, 0.0, 0]
a = [3.5668, 17.8373, 29.838373, 13.5, 13.5, 10, 12.5, 2.9, 0, 0, 0]
b = [11.63535, 46.383838, 23.18827, 18.9833, 2, 2, 0, 0, 0, 0, 0]
labels = ['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-2.5',
          '2.5-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5', '5-5.5']


x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, a, width, label='Trilateration')
rects2 = ax.bar(x + width/2, b, width, label='Fingerprint')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Tỉ lệ (%)')
ax.set_xlabel('Sai số (m)')
# ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

fig.tight_layout()

plt.show()
