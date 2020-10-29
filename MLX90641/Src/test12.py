# 计算每一列的平均值展示
# 基于"data01.npy" 200farme有人
# mlx90641
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.subscribe as subscribe

data01 = np.load("../Dataset/data01.npy")


def receiveMqtt():
    msg = subscribe.simple("test", hostname="192.168.1.120")
    msg = str(msg.payload)
    msg_list = msg.split(sep=",")
    msg_list = msg_list[1:193]
    piexls = []
    for i in msg_list:
        piexls.append(float(i))
    piexls1 = np.array(piexls)
    return piexls1


class Frame():
    def __init__(self, piexls):
        # piexls 12x16 np数组
        self.piexls = piexls
        self.piexls_mean = piexls.mean()
        self.col_mean = self.colmean()
        self.col_media = self.colmedia()
        self.col_diff = self.diff()
        self.index = self.index()
    def colmean(self):
        piexls = self.piexls
        col_mean = np.ones(16)
        for i in range(16):
            col_mean[i] = piexls[:, i].mean()
        return col_mean

    def colmedia(self):
        piexls = self.piexls
        col_media = np.ones(16)
        for i in range(16):
            col_media[i] = np.median(piexls[:, i])
            # col_media[i] = piexls[:, i].median()
        return col_media

    def diff(self):
        col = self.col_mean
        # col = self.col_media
        col_diff = np.ones(16)
        col_diff[0] = abs(4 * col[0] - col[1] - col[2] - 2 * self.piexls_mean)
        col_diff[1] = abs(4 * col[1] - col[2] - col[3] - 2 * self.piexls_mean)
        col_diff[14] = abs(4 * col[14] - col[12] - col[13] - 2 * self.piexls_mean)
        col_diff[15] = abs(4 * col[15] - col[14] - col[13] - 2 * self.piexls_mean)
        for i in range(2, 14):
            col_diff[i] = abs(4 * col[i % 16] - col[(i + 1) % 16] - col[(i - 1) % 16] - col[(i + 2) % 16] - col[
                (i - 2) % 16])
        # col_diff[0] = 0
        # col_diff[-1] = 0
        return col_diff

    def point_one(self):
        col = self.col_diff
        one_index = col.index(max(col))
        return one_index

    def points_index(self):
        col = self.col_diff
        index_list = list
        for i in range(2, 14):
            if (col[i] > col[i - 1] and col[i] > col[i + 1]):
                index_list.append(i)
        return index_list

class Track():
    def __init__(self):
        self.flag = 0
        #  0: error
        # +1:  in
        # -1:  out
        self.pointList = [0]
        # 轨迹行数列表
        self.exist = 0  # 当前处于有效轨迹中
        self.num = 0
        # 室内人数


fig, ax = plt.subplots()
col = np.ones(16)
for i in range(100000):
    ax.cla()
    # piexls = data01[i]
    piexls = receiveMqtt()
    piexls.resize(12, 16)
    F = Frame(piexls)
    col = F.col_diff
    col_img = col.copy()
    col_img.resize(1, 16)
    # ax.imshow(col_img, vmin=20, vmax=30)
    ax.imshow(col_img, vmin=2, vmax=5)
    # ax.imshow(piexls, cmap="gray", vmin=20, vmax=35)
    # ax.imshow(data[i])
    ax.set_title("frame {}".format(i))
    # Note that using time.sleep does *not* work here!
    plt.pause(0.01)
#
# np.save("data01.npy",data)