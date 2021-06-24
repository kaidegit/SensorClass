import numpy as np


def solution(x_list, y_list, d_list):
    l = []
    l.append(
        d_list[1] ** 2 - d_list[0] ** 2
        - x_list[1] ** 2 + x_list[0] ** 2
        - y_list[1] ** 2 + y_list[0] ** 2
    )
    l.append(
        d_list[2] ** 2 - d_list[0] ** 2
        - x_list[2] ** 2 + x_list[0] ** 2
        - y_list[2] ** 2 + y_list[0] ** 2
    )
    A = [
        [2 * (x_list[0] - x_list[1]), 2 * (y_list[0] - y_list[1])],
        [2 * (x_list[0] - x_list[2]), 2 * (y_list[0] - y_list[2])]
    ]
    A = np.mat(np.array(A))
    A = A.I
    l = np.mat(np.array(l))
    l = l.T
    return (A * l).tolist()


x_full_list = [0, 300, 300, 0]
y_full_list = [0, 0, 360, 360]
# d_full_list = [261, 293, 218, 154]
d_full_list = [[261, 293, 218, 154],
               [262, 295, 217, 154],
               [261, 295, 217, 155],
               [261, 295, 217, 155],
               [263, 295, 214, 155],
               [262, 295, 213, 156],
               [262, 293, 214, 156],
               [261, 294, 214, 161],
               [261, 296, 214, 160],
               [260, 297, 215, 160]]

for d_each_list in d_full_list:
    x = 0
    y = 0
    for i in range(4):
        x_temp_list = x_full_list.copy()
        del x_temp_list[i]
        y_temp_list = y_full_list.copy()
        del y_temp_list[i]
        d_temp_list = d_each_list.copy()
        del d_temp_list[i]
        ret = solution(x_temp_list, y_temp_list, d_temp_list)
        print(int(ret[0][0] + 0.5), int(ret[1][0] + 0.5), sep=',', end='\t')
        x += ret[0][0]
        y += ret[1][0]
    print(int(x / 4 + 0.5), int(y / 4 + 0.5), sep=',')
